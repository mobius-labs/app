<template>
    <div class="is-flex is-align-items-stretch is-full-height">
        <div class="is-flex-1 is-relative is-flex is-flex-direction-column">
            <div class="app-header">
                <h1 class="title">Contacts</h1>
                <div class="ml-6 mr-4">
                    <o-input
                        :model-value="searchQuery"
                        type="search"
                        icon="search"
                        placeholder="Search for contacts..."
                        @update:model-value="debounceUpdateSearchQuery"
                    />
                </div>

                <div class="is-flex-grow-1"></div>

                <o-button
                    variant="primary"
                    icon-left="plus"
                    :disabled="isAddContactButtonDisabled"
                    @click="addContact"
                    >Add Contact</o-button
                >
            </div>

            <o-loading :active="loading" :full-page="false">
                <Spinner size="large"></Spinner>
            </o-loading>

            <!-- TODO: make this header sticky -->
            <o-table hoverable focusable :data="filteredContacts">
                <o-table-column v-slot="props" label="Name">
                    {{ getFullName(props.row.contact) }}
                </o-table-column>
                <o-table-column v-slot="props" label="Phone Nos. & Emails">
                    <ContactsOneToManyList
                        v-slot="{ item }"
                        api-name="email"
                        :contact-id="props.row.contact.id"
                        :version="props.row.version"
                    >
                        <span class="tag mr-2"
                            ><o-icon icon="envelope" class="mr-0" /><a
                                :href="'mailto:' + item.email_address"
                                class="has-text-grey-darker"
                                >{{ item.email_address }}</a
                            ></span
                        >
                    </ContactsOneToManyList>

                    <ContactsOneToManyList
                        v-slot="{ item }"
                        api-name="phone_no"
                        :contact-id="props.row.contact.id"
                        :version="props.row.version"
                    >
                        <span class="tag mr-2"
                            ><o-icon icon="phone" class="mr-0" />{{
                                item.number
                            }}</span
                        >
                    </ContactsOneToManyList>
                </o-table-column>
                <o-table-column v-slot="props" label="Address">
                    <ContactsOneToManyList
                        v-slot="{ item }"
                        api-name="address"
                        :contact-id="props.row.contact.id"
                        :version="props.row.version"
                    >
                        <p class="is-size-7">
                            {{ item.address_line_one }}<br />{{
                                item.address_line_two
                            }}<br />{{ item.suburb }} {{ item.state }}
                            {{ item.postcode }}
                        </p>
                    </ContactsOneToManyList>
                </o-table-column>
                <o-table-column
                    v-if="selectedId === null"
                    v-slot="props"
                    label="Regularity of Contact"
                >
                    {{
                        displayRegularity(
                            props.row.contact.regularity_of_contact
                        )
                    }}
                </o-table-column>
                <o-table-column v-slot="props" label="Actions">
                    <div class="buttons">
                        <o-button
                            icon-left="pencil-alt"
                            variant="warning"
                            @click="
                                $router.push(
                                    '/app/contacts/' + props.row.contact.id
                                )
                            "
                        >
                            Edit
                        </o-button>

                        <o-button
                            icon-left="trash"
                            variant="info"
                            @click="deleteContact(props.row.localId)"
                        >
                            Delete
                        </o-button>
                    </div>
                </o-table-column>
            </o-table>
        </div>

        <div
            :class="{ 'edit-contacts': true, expanded: isContactsEditExpanded }"
        >
            <ContactsEdit
                v-if="isContactsEditExpanded"
                ref="contactsEdit"
                :local-id="selectedLocalId"
                :server-id="selectedServerId"
                :is-discard-changes-dialog-active="isDiscardChangesDialogActive"
                @contact-updated="onContactUpdated"
                @discard-changes="discardChanges"
                @cancel-discard="isDiscardChangesDialogActive = false"
            />
        </div>
    </div>
</template>

<script lang="ts">
import ContactsEdit from "../components/ContactsEdit.vue";
import { Options, Vue } from "vue-class-component";
import {
    Contact,
    ContactId,
    displayRegularity,
    getFullName,
} from "@/api/contacts";
import { getAxiosInstance } from "@/api/api";
import { defaultToast } from "@/toasts";
import Spinner from "../components/Spinner.vue";
import ContactsOneToManyList from "@/components/ContactsOneToManyList.vue";
import { debounce, deepCopy } from "@/api/utils";

class Props {
    selectedId: number | null = null;
}

interface LocalContact {
    contact: Contact;
    localId: ContactId;
    // when this version # is incremented, the contact will refresh from the server
    version: number;
}

@Options({
    components: { ContactsEdit, Spinner, ContactsOneToManyList },
    watch: { searchQuery: "loadAllContacts" },
})
export default class Contacts extends Vue.with(Props) {
    searchQuery = "";
    contacts = new Map<ContactId, LocalContact>();
    nextClientContactId = -1;
    getFullName = getFullName;
    displayRegularity = displayRegularity;
    isDiscardChangesDialogActive = false;
    loading = false;
    nextFn: () => void = () => {};

    debounceUpdateSearchQuery = debounce((v: string) => {
        this.searchQuery = v;
    }, 500);

    static NEW_CONTACT = -1;

    get filteredContacts() {
        return Array.from(this.contacts.values());
    }

    async mounted() {
        await this.loadAllContacts();
    }

    get isContactsEditExpanded() {
        return this.selectedId !== null;
    }

    get isAddContactButtonDisabled() {
        return this.selectedId === Contacts.NEW_CONTACT;
    }

    get selectedLocalId() {
        if (this.selectedId === Contacts.NEW_CONTACT) {
            return this.nextClientContactId;
        }
        for (let contact of this.contacts.values()) {
            if (contact.contact.id === this.selectedId) {
                return contact.localId;
            }
        }
        return this.selectedId;
    }

    get selectedServerId() {
        return this.selectedId === Contacts.NEW_CONTACT
            ? null
            : this.selectedId;
    }

    hasUnsavedChanges(): boolean {
        return this.$refs.contactsEdit
            ? (this.$refs.contactsEdit as ContactsEdit).hasUnsavedChanges()
            : false;
    }

    async loadAllContacts() {
        this.loading = true;
        let response = await getAxiosInstance().get("contact_book/list", {
            params: { search: this.searchQuery },
        });
        this.contacts.clear();
        for (let contact of response.data.results) {
            this.contacts.set(contact.id, {
                contact,
                localId: contact.id,
                version: 1,
            });
        }
        this.loading = false;
    }

    async deleteContact(id: ContactId) {
        let contact = this.contacts.get(id);
        if (contact) {
            try {
                await getAxiosInstance().delete(
                    "contact_book/delete_contact_by_id/" + contact.contact.id
                );
                this.$oruga.notification.open(
                    defaultToast("info", "Contact deleted")
                );
                this.contacts.delete(id);
            } catch (e) {
                this.$oruga.notification.open(
                    defaultToast("danger", "Failed to delete contact")
                );
            }
        }
    }

    // updates the contact info for a particular contact in-place,
    // without reloading all the contacts from scratch
    onContactUpdated(localId: ContactId, contact: Contact) {
        console.log("Contacts: received updated event for ", localId);
        let existing = this.contacts.get(localId);
        this.contacts.set(localId, {
            contact: deepCopy(contact),
            localId: localId,
            version: existing ? existing.version + 1 : 1,
        });
    }

    addContact() {
        this.nextClientContactId--;
        this.$router.push("/app/contacts/new");
    }

    checkForUnsavedChanges(next: () => void) {
        if (this.hasUnsavedChanges()) {
            this.isDiscardChangesDialogActive = true;
            this.nextFn = next;
            return;
        }
        next();
    }

    discardChanges() {
        this.isDiscardChangesDialogActive = false;
        this.nextFn();
    }

    beforeRouteUpdate(to: any, from: any, next: () => void) {
        this.checkForUnsavedChanges(next);
    }

    beforeRouteLeave(to: any, from: any, next: () => void) {
        this.checkForUnsavedChanges(next);
    }

    created() {
        window.addEventListener("beforeunload", this.beforeWindowUnload);
    }

    beforeDestroy() {
        window.removeEventListener("beforeunload", this.beforeWindowUnload);
    }

    // if the user tries to close the tab / force refresh the page,
    // check for unsaved changes
    beforeWindowUnload(e: BeforeUnloadEvent) {
        if (this.hasUnsavedChanges()) {
            e.preventDefault();
            e.returnValue = "";
        }
    }
}
</script>

<style scoped>
.app-header {
    padding: 2rem;
    display: flex;
}

.is-full-height {
    height: 100%;
}

.is-flex-1 {
    flex: 1;
}

.edit-contacts {
    overflow-y: auto;
    width: 0;
    flex: 0;
    transition: width 0.2s ease, flex 0.2s ease;
    border-left: 1px solid #ccc;
}

.expanded {
    min-width: 30rem;
    flex: 1;
}

:deep(.b-table.table-wrapper) {
    height: 300px;
    overflow-y: scroll;
    flex: 1 1 auto;
}
</style>
