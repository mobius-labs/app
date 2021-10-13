<template>
    <div class="mb-5">
        <p class="subtitle mb-2" data-test="title">
            {{ title }}
            <button
                class="button is-warning is-small ml-3"
                data-test="add-button"
                style="text-decoration: none"
                @click="addItem"
            >
                <o-icon icon="plus"></o-icon><span>{{ addButtonText }}</span>
            </button>
        </p>

        <div
            v-for="[id, model] of items.entries()"
            :key="JSON.stringify(id)"
            class="is-flex is-align-items-start space-items"
        >
            <slot
                :model="model"
                :update-item="(v) => updateItem(id, v)"
                :debounce-update-item="(v) => debounceUpdateItem(id, v)"
                :delete-item="() => deleteItem(id)"
            ></slot>
            <button
                class="delete mt-3 ml-2"
                data-test="delete-button"
                @click="deleteItem(id)"
            ></button>
            <span
                :class="{
                    'is-size-7': true,
                    'mt-3': true,
                    'ml-3': true,
                    'has-text-success': statusMessages.get(id).successMessage,
                    'has-text-danger': statusMessages.get(id).dangerMessage,
                }"
                style="width: 4rem"
            >
                {{
                    statusMessages.get(id).successMessage
                        ? statusMessages.get(id).successMessage
                        : statusMessages.get(id).dangerMessage
                }}
            </span>
        </div>
    </div>
</template>

<script lang="ts">
import { debounce, delay } from "@/api/utils";
import { Options, prop, Vue } from "vue-class-component";
import { getAxiosInstance } from "@/api/api";
import { defaultToast } from "@/toasts";
import { Model } from "@/api/model";
import { ContactId, ServerContactId } from "@/api/contacts";
import { PropType } from "vue";

class Props {
    title!: string;
    addButtonText!: string;
    localId = prop({
        type: Number as PropType<ContactId>,
        required: true,
    });
    serverId = prop({
        type: Number as PropType<ServerContactId>,
        default: null,
    });
    freshItem!: () => Record<string, any>;
    apiName!: string;
}

// negative numbers are "client IDs", specific to this component,
// positive numbers are actual IDs registered with the server.
type ItemId = number;

class Status {
    dangerMessage: string = "";
    successMessage: string = "";
}

// ContactsOneToMany abstracts over all of the one-to-many relationships which a contact has.
// It allows for CRUD operations on those nested models (e.g.: addresses, phone numbers)
//
// When we first create an item, it gets a client id (local to this editing session)
// we can use it to identify items in the list
// as soon as the user types something, we try to POST the object to the server, and receive a
// server ID, which we then continue to use for future PUT updates
@Options({
    emits: ["update:saving"],
    watch: { localId: "fetchAllItems" },
})
export default class ContactsOneToMany extends Vue.with(Props) {
    items: Map<ItemId, Model> = new Map<ItemId, Model>();

    nextClientId = -1;
    recentlyUpdated: Set<ItemId> = new Set<ItemId>();
    queuedUpdates: Set<ItemId> = new Set<ItemId>();

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

    get firstLetterOfApiName() {
        return this.apiName[0];
    }

    // onServerIdUpdated(newId: ServerContactId, oldId: ServerContactId) {
    //     console.log(oldId, '->', newId);
    //     if (!newId || oldId) {
    //         return;
    //     }
    //
    //     // we now have a server ID, let's try and POST all the items
    //     console.log('ContactsOneToMany: trying to POST all items');
    //     for (const [id, entry] of this.items.entries()) {
    //         if(!entry.matchesServer()) {
    //             this.updateItemOnServer(id)
    //         }
    //     }
    // }

    async fetchAllItems() {
        this.items.clear();
        if (!this.serverId) {
            return;
        }
        let response = await getAxiosInstance().get(
            "/contact_book/get_" + this.apiName + "s_by_cid/" + this.serverId
        );
        for (let item of response.data) {
            this.items.set(item.id, new Model(item));
        }
    }

    async mounted() {
        await this.fetchAllItems();
    }

    clearRecentlyUpdatedAfterDelay = debounce((id: ItemId) => {
        this.recentlyUpdated.delete(id);
    }, 3000);

    markRecentlyUpdated(itemId: ItemId) {
        this.recentlyUpdated.add(itemId);
        this.clearRecentlyUpdatedAfterDelay(itemId);
    }

    addItem() {
        let freshItem = this.freshItem();
        this.items.set(this.nextClientId--, new Model(freshItem));
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

        this.maybeStopSaving();

        // if any new requests to update the item came in whilst we were waiting for a server response,
        // then dispatch those now...
        if (this.queuedUpdates.has(itemId)) {
            console.log("ContactsOneToMany: dispatching update request...");
            this.queuedUpdates.delete(itemId);
            await this.updateItemOnServer(itemId);
        }
    }

    async updateItemOnServer(itemId: ItemId): Promise<void> {
        console.log("server id", this.$props.serverId, this.serverId);
        if (!this.serverId) {
            console.log(
                "ContactsOneToMany: aborting update since parent model doesnt exist yet",
                this.serverId
            );
            return;
        }

        let model = this.items.get(itemId);
        if (!model) {
            console.log(
                "ContactsOneToMany: aborting update since model has disappeared"
            );
            return;
        }

        if (model.isSubmitting) {
            console.log("ContactsOneToMany: queuing update request...");
            this.queuedUpdates.add(itemId);
            return;
        }
        // we want to never send more than one request at a time for this item id...
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
                        : "/" + this.serverId),
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
        if (!item) {
            console.warn(
                "ContactsOneToMany: attempting to delete non-existent item ",
                id,
                this.items
            );
            return;
        }
        this.items.delete(id);
        if (this.serverId === null || !item.model.id) {
            // nothing to delete
            return;
        }

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
            console.error(e);
            this.$oruga.notification.open(
                defaultToast("danger", "Failed to delete item")
            );
            return;
        }
        await this.markRequestFinished(id);
    }

    debounceUpdateItem = debounce(this.updateItem.bind(this), 700);

    async updateItem(id: ItemId, newValue: Record<string, any>) {
        console.log("ContactsOneToMany: request to update", id, newValue);
        let item = this.items.get(id);
        if (!item) {
            return;
        }
        item.model = {
            ...item.model,
            ...newValue,
        };
        await this.updateItemOnServer(id);
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

<style scoped>
:deep(.space-items > *) {
    margin-right: 0.5rem;
}
</style>
