<template>
    <div
        class="is-flex is-align-items-stretch is-full-height"
        style="position: absolute; left: 0; top: 0; width: 100%"
        :data-expanded="isContactsEditExpanded"
    >
        <div class="right-flyout-main is-flex is-flex-direction-column">
            <div class="app-header">
                <h1 class="title">Contacts</h1>

                <div class="is-flex-grow-1"></div>

                <div class="ml-3 mr-3">
                    <o-input
                        :model-value="searchQuery"
                        type="search"
                        icon="search"
                        placeholder="Search for contacts..."
                        @update:model-value="debounceUpdateSearchQuery"
                    />
                </div>

                <o-button
                    tag="router-link"
                    to="/app/scan-card"
                    variant="info"
                    icon-left="camera"
                    class="mr-3"
                    >Scan Business Card</o-button
                >

                <o-button
                    variant="primary"
                    icon-left="plus"
                    :disabled="isAddContactButtonDisabled"
                    @click="addContact"
                    >Add Contact</o-button
                >
            </div>

            <div class="is-relative is-flex-1 is-flex-direction-column is-flex">
                <o-loading :active="loading" :full-page="false">
                    <Spinner size="large"></Spinner>
                </o-loading>

                <!-- TODO: make this header sticky -->
                <!-- TODO: make page size derived from server -->
                <o-table
                    hoverable
                    focusable
                    paginated
                    backend-pagination
                    backend-sorting
                    :data="contacts"
                    v-model:current-page="currentPage"
                    @sort="onSortChanged"
                    :per-page="10"
                    :total="totalContacts"
                >
                    <o-table-column
                        v-slot="props"
                        label="First Name"
                        field="first_name"
                        sortable
                        v-if="!isContactsEditExpanded"
                    >
                        {{ props.row.contact.first_name }}
                    </o-table-column>
                    <o-table-column
                        v-slot="props"
                        label="Surname"
                        field="surname"
                        sortable
                        v-if="!isContactsEditExpanded"
                    >
                        {{ props.row.contact.surname }}
                    </o-table-column>
                    <o-table-column
                        v-slot="props"
                        label="Name"
                        v-if="isContactsEditExpanded"
                    >
                        {{ getFullName(props.row.contact) }}
                    </o-table-column>
                    <o-table-column v-slot="props" label="Phone Nos. & Emails">
                        <span
                            class="tag mr-2"
                            v-for="item in props.row.contact.emails"
                            :key="item.id"
                            ><o-icon icon="envelope" class="mr-0" /><a
                                :href="'mailto:' + item.email_address"
                                class="has-text-grey-darker"
                                >{{ item.email_address }}</a
                            ></span
                        >

                        <span
                            class="tag mr-2"
                            v-for="item in props.row.contact.phone_nos"
                            :key="item.id"
                            ><o-icon icon="phone" class="mr-0" />{{
                                item.number
                            }}</span
                        >
                    </o-table-column>
                    <o-table-column v-slot="props" label="Address">
                        <p
                            class="is-size-7"
                            v-for="item in props.row.contact.addresses"
                            :key="item.id"
                        >
                            {{ item.address_line_one }}<br />{{
                                item.address_line_two
                            }}<br />{{ item.suburb }}
                            {{ item.state }}
                            {{ item.postcode }}
                        </p>
                    </o-table-column>
                    <o-table-column
                        v-if="!isContactsEditExpanded"
                        v-slot="props"
                        label="Regularity of Contact"
                        field="regularity_of_contact"
                        sortable
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
                    <template #empty>
                        <p>No results found.</p>
                    </template>
                    <!-- TODO: when https://github.com/oruga-ui/oruga/issues/208 is fixed,
                               try to fix pagination to the bottom of the window -->
                    <!--                <template #footer>-->
                    <!--                    <tr>Footer</tr>-->
                    <!--                </template>-->
                </o-table>
            </div>
        </div>

        <div class="right-flyout">
            <ContactsEdit
                v-if="isContactsEditExpanded"
                ref="contactsEdit"
                :local-id="selectedLocalId"
                :initial-data="initialData"
                :server-id="selectedServerId"
                @close="onContactEditClosed"
                @contact-updated="onContactUpdated"
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
    FullContact,
    getFullName,
    ServerContactId,
} from "@/api/contacts";
import { getAxiosInstance, ListResponse } from "@/api/api";
import { defaultToast } from "@/toasts";
import Spinner from "../components/Spinner.vue";
import debounce from "lodash/debounce";

class Props {
    selectedId: number | null = null;
    initialData?: FullContact;
}

interface LocalContact {
    contact: Contact;
    localId: ContactId;
    // when this version # is incremented, the contact will refresh from the server
    version: number;
}

type ContactsListResponse = ListResponse<Contact>;

interface SortData {
    field: string;
    direction: "asc" | "desc";
}

@Options({
    components: { ContactsEdit, Spinner },
    watch: {
        searchQuery: "loadAllContacts",
        currentPage: "loadAllContacts",
        sortData: "loadAllContacts",
    },
})
export default class Contacts extends Vue.with(Props) {
    searchQuery = "";
    contacts: LocalContact[] = [];
    sortData: SortData | null = null;
    totalContacts = 0;
    currentPage = 1;
    nextClientContactId = -1;
    getFullName = getFullName;
    displayRegularity = displayRegularity;
    loading = false;
    serverToLocalIdMap = new Map<ServerContactId, ContactId>();

    debounceUpdateSearchQuery = debounce((v: string) => {
        this.searchQuery = v;
    }, 500);

    static NEW_CONTACT = -1;

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
        return this.serverToLocalIdMap.get(this.selectedId) || this.selectedId;
    }

    get selectedServerId() {
        return this.selectedId === Contacts.NEW_CONTACT
            ? null
            : this.selectedId;
    }

    get orderingParam() {
        if (!this.sortData) {
            return null;
        }
        return this.sortData.direction === "asc"
            ? this.sortData.field
            : "-" + this.sortData.field;
    }

    findContactById(localId: ContactId): LocalContact | null {
        for (const contact of this.contacts) {
            if (contact.localId === localId) {
                return contact;
            }
        }
        return null;
    }

    async loadAllContacts() {
        this.loading = true;
        const response = await getAxiosInstance().get("contact_book/list", {
            params: {
                search: this.searchQuery,
                page: this.currentPage,
                ordering: this.orderingParam,
            },
        });
        const data = response.data as ContactsListResponse;

        this.totalContacts = data.count;

        this.contacts = data.results.map((serverContact: Contact) => {
            const localId =
                this.serverToLocalIdMap.get(serverContact.id!) ||
                serverContact.id!;
            const localContact = this.findContactById(localId);

            return {
                contact: serverContact,
                localId,
                version: localContact ? localContact.version : 1,
            };
        });
        this.loading = false;
    }

    async deleteContact(id: ContactId) {
        const contact = this.findContactById(id);
        if (contact) {
            try {
                await getAxiosInstance().delete(
                    "contact_book/delete_contact_by_id/" + contact.contact.id
                );
                this.$oruga.notification.open(
                    defaultToast("info", "Contact deleted")
                );
                await this.loadAllContacts();
            } catch (e) {
                this.$oruga.notification.open(
                    defaultToast("danger", "Failed to delete contact")
                );
            }
        }
    }

    // updates the contact info for a particular contact in-place,
    // without reloading all the contacts from scratch
    async onContactUpdated(
        localId: ContactId,
        serverId: ServerContactId,
        newlyCreated: boolean
    ) {
        console.log("Contacts: received updated event for ", localId, serverId);
        if (serverId !== null) {
            this.serverToLocalIdMap.set(serverId, localId);
        }
        const contact = this.findContactById(localId);
        if (contact) {
            contact.version += 1;
        }
        await this.loadAllContacts();
        if (newlyCreated) {
            await this.$router.push("/app/contacts/" + serverId);
        }
    }

    onContactEditClosed() {
        this.$router.push("/app/contacts");
    }

    onSortChanged(field: string, direction: "asc" | "desc") {
        this.sortData = { field, direction };
    }

    addContact() {
        this.nextClientContactId--;
        this.$router.push("/app/contacts/new");
    }

    async mounted() {
        await this.loadAllContacts();
    }

    beforeRouteUpdate(to: any, from: any, next: () => void) {
        if (this.$refs.contactsEdit) {
            (
                this.$refs.contactsEdit as typeof ContactsEdit
            ).checkForUnsavedChanges(next);
        } else {
            next();
        }
    }

    beforeRouteLeave(to: any, from: any, next: () => void) {
        if (this.$refs.contactsEdit) {
            (
                this.$refs.contactsEdit as typeof ContactsEdit
            ).checkForUnsavedChanges(next);
        } else {
            next();
        }
    }
}
</script>

<style scoped>
@import "../styles/flyout.scss";

.app-header {
    padding: 2rem;
    display: flex;
}

@media screen and (max-width: 1900px) {
    .app-header {
        flex-wrap: wrap;
        justify-content: flex-end;
    }
}

.is-full-height {
    height: 100%;
}

.is-flex-1 {
    flex: 1;
}

:deep(.b-table.table-wrapper) {
    height: 300px;
    overflow-y: scroll;
    flex: 1 1 auto;
}

:deep(.pagination) {
    padding: 8px;
}
</style>
