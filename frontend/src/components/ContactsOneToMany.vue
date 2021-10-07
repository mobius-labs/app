<template>
    <div class="mb-3">
        <p class="subtitle">{{ title }}</p>

        <div
            v-for="[id, model] of items.entries()"
            :key="JSON.stringify(id)"
            class="is-flex is-align-items-start"
        >
            <slot
                :model="model"
                :update-item="(v) => updateItem(id, v)"
                :debounce-update-item="(v) => debounceUpdateItem(id, v)"
                :delete-item="() => deleteItem(id)"
            ></slot>
            <div class="is-size-7 mt-3 ml-3">
                <progress
                    v-if="statusMessages.get(id).isProgress"
                    class="progress is-small is-info"
                    max="100"
                ></progress>
                <span
                    v-else-if="statusMessages.get(id).successMessage"
                    class="has-text-success"
                    >{{ statusMessages.get(id).successMessage }}</span
                >
                <span
                    v-else-if="statusMessages.get(id).dangerMessage"
                    class="has-text-danger"
                    >{{ statusMessages.get(id).dangerMessage }}</span
                >
            </div>
        </div>

        <o-button
            class="add-item"
            variant="success"
            size="small"
            @click="addItem"
            >{{ addButtonText }}</o-button
        >
    </div>
</template>

<script lang="ts">
import { debounce, delay } from "@/api/utils";
import { Options, Vue } from "vue-class-component";
import { getAxiosInstance, Model } from "@/api/api";
import { defaultToast } from "@/toasts";

class Props {
    title!: string;
    addButtonText!: string;
    contactId!: number | null;
    freshItem!: () => Record<string, any>;
    apiName!: string;
    // If this flag is true, then emails/phones/socials/address will *not*
    // be refreshed when contactId changes.
    // eslint-disable-next-line no-unused-vars
    skipReload!: (a: number | null) => boolean;
}

interface ServerId {
    kind: "server";
    id: number;
}

interface ClientId {
    kind: "client";
    id: number;
}

type ItemId = ClientId | ServerId;

class Status {
    dangerMessage: string = "";
    successMessage: string = "";
    isProgress: boolean = false;
}

// when we first create an item, it gets a client id (local to this editing session)
// we can use it to identify items in the list
// as soon as the user types something, we try to POST the object to the server, and receive a
// server ID, which we then continue to use.
@Options({
    emits: ["update:saving"],
    watch: { contactId: "onContactIdUpdated" },
})
export default class ContactsOneToMany extends Vue.with(Props) {
    items: Map<ItemId, Model> = new Map<ItemId, Model>();

    clientId = 1;
    recentlyUpdated: Set<ItemId> = new Set<ItemId>();
    queuedUpdates: Set<ItemId> = new Set<ItemId>();

    get firstLetterOfApiName() {
        return this.apiName[0];
    }

    get statusMessages() {
        let entries: [ItemId, Status][] = Array.from(this.items).map(
            ([id, model]: [ItemId, Model]) => {
                let status = new Status();
                if (model.nonFieldErrors.length > 0) {
                    status.dangerMessage = model.nonFieldErrors.join(", ");
                } else if (this.recentlyUpdated.has(id)) {
                    status.successMessage = "Updated";
                }
                return [id, status];
            }
        );
        return new Map<ItemId, Status>(entries);
    }

    async onContactIdUpdated(newId: number | null, oldId: number | null) {
        if (this.skipReload(newId)) {
            // instead of reloading items FROM the server,
            // we try and POST all items TO the server.
            console.warn("skipping list reload since skip-reload=true");
            await this.postAll();
            return;
        }
        console.log(newId, oldId);
        if (newId === oldId) {
            return;
        }
        await this.fetchAllItems();
    }

    async fetchAllItems() {
        if (!this.contactId) {
            this.items.clear();
            return;
        }
        console.log("reloading", this.apiName);
        let response = await getAxiosInstance().get(
            "/contact_book/get_" + this.apiName + "s_by_cid/" + this.contactId
        );
        console.log("loaded", this.apiName, "items", response.data);
        for (let item of response.data) {
            this.items.set({ kind: "server", id: item.id }, new Model(item));
        }
    }

    async mounted() {
        await this.fetchAllItems();
    }

    clearRecentlyUpdatedAfterDelay = debounce((id: ItemId) => {
        console.log("clear updated");
        this.recentlyUpdated.delete(id);
    }, 3000);

    markRecentlyUpdated(itemId: ItemId) {
        console.log("added updated");
        this.recentlyUpdated.add(itemId);
        this.clearRecentlyUpdatedAfterDelay(itemId);
    }

    addItem() {
        let freshItem = this.freshItem();
        this.items.set(
            { kind: "client", id: this.clientId++ },
            new Model(freshItem)
        );
    }

    markRequestAsInFlight(model: Model) {
        model.isSubmitting = true;
        this.$emit("update:saving", true);
    }

    maybeStopSaving() {
        let updating = false;
        for (let item of this.items.values()) {
            if (item.isSubmitting) {
                updating = true;
                break;
            }
        }
        if (!updating) {
            this.$emit("update:saving", false);
        }
    }

    async markRequestFinished(itemId: ItemId) {
        // this delay is just to make the UI 'feel' better
        await delay(700);
        let item = this.items.get(itemId);
        if (item) {
            item.isSubmitting = false;
        }

        // if any new requests to update the item came in whilst we were waiting for a server response,
        // then dispatch those now...
        if (this.queuedUpdates.has(itemId)) {
            console.log("dispatching update request...");
            this.queuedUpdates.delete(itemId);
            await this.updateItemOnServer(itemId);
        }
    }

    async updateItemOnServer(itemId: ItemId): Promise<void> {
        if (!this.contactId) {
            console.log(
                "aborting update since parent model doesnt exist yet",
                this.contactId
            );
            return;
        }

        let model = this.items.get(itemId);
        if (!model) {
            console.log("aborting update since model has disappeared");
            return;
        }

        // let model = this.items.get()
        if (model.isSubmitting) {
            console.log("queuing update request...");
            this.queuedUpdates.add(itemId);
            return;
        }
        // want to never send more than one request at a time for this item id...
        this.markRequestAsInFlight(model);
        let error = undefined;
        try {
            let response = await getAxiosInstance().request({
                url:
                    "/contact_book/" +
                    (model.model.id ? "update_" : "create_") +
                    this.apiName +
                    (model.model.id
                        ? "_by_" +
                          this.firstLetterOfApiName +
                          "id/" +
                          model.model.id
                        : "/" + this.contactId),
                method: model.model.id ? "PUT" : "POST",
                data: model.model,
            });
            if (response.data.id) {
                // let's add the id from the server...
                model.model.id = response.data.id;
            }
            this.markRecentlyUpdated(itemId);
        } catch (e) {
            error = e;
            console.warn(e);
        }
        model.captureServerResponse(null, error);

        await this.markRequestFinished(itemId);
    }

    async deleteItem(id: ItemId) {
        let item = this.items.get(id);
        this.items.delete(id);
        if (this.contactId !== null && item && item.model.id) {
            this.markRequestAsInFlight(item);
            try {
                await getAxiosInstance().delete(
                    "/contact_book/delete_" +
                        this.apiName +
                        "_by_" +
                        this.firstLetterOfApiName +
                        "id/" +
                        item.model.id
                );
            } catch (e) {
                this.$oruga.notification.open(
                    defaultToast("danger", "Failed to delete item")
                );
                return;
            }
            await this.markRequestFinished(id);
        }
    }

    debounceUpdateItem = debounce(
        (id: ItemId, newValue: Record<string, any>) => {
            this.updateItem(id, newValue);
        },
        700
    );

    async updateItem(id: ItemId, newValue: Record<string, any>) {
        console.log("request to update", id.kind + "#" + id.id);
        let item = this.items.get(id);
        if (!item) {
            return;
        }
        for (const [key, value] of Object.entries(newValue)) {
            item.model[key] = value;
        }
        await this.updateItemOnServer(id);
    }

    async postAll() {
        let promises = [];
        for (let id of this.items.keys()) {
            promises.push(this.updateItemOnServer(id));
        }
        return Promise.all(promises);
    }

    hasUnsavedChanges() {
        if (this.queuedUpdates.size > 0) {
            return true;
        }
        for (let model of this.items.values()) {
            if (model.hasErrors()) {
                return true;
            }
        }
        return false;
    }
}
</script>

<style scoped></style>
