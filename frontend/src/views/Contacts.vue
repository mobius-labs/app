<template>
    <div class="is-flex is-align-items-stretch is-full-height">
        <div class="contacts-list is-relative is-flex is-flex-direction-column">
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
                    :disabled="selectedId == -1"
                    @click="openNewContactPane"
                    >Add Contact</o-button
                >
            </div>

            <o-loading :active="loading" :full-page="false">
                <Spinner size="large"></Spinner>
            </o-loading>

            <!-- TODO: make this header sticky -->
            <o-table hoverable focusable :data="filteredContacts">
                <o-table-column v-slot="props" label="Name">
                    {{ getFullName(props.row) }}
                </o-table-column>
                <o-table-column v-slot="props" label="Phone Nos. & Emails">
                    <ContactsOneToManyList
                        v-slot="{ item }"
                        api-name="email"
                        :contact-id="props.row.id"
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
                        :contact-id="props.row.id"
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
                        :contact-id="props.row.id"
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
                    {{ displayRegularity(props.row.regularity_of_contact) }}
                </o-table-column>
                <!--                <o-table-column-->
                <!--                    v-if="selectedId === null"-->
                <!--                    v-slot="props"-->
                <!--                    label="Social Media"-->
                <!--                >-->
                <!--                    <span v-if="props.row.facebook" class="tag is-link"-->
                <!--                        ><o-icon-->
                <!--                            icon="facebook"-->
                <!--                            pack="fab"-->
                <!--                            class="mr-0"-->
                <!--                        ></o-icon-->
                <!--                        >{{ props.row.facebook }}</span-->
                <!--                    >-->
                <!--                    <span v-if="props.row.instagram" class="tag is-link"-->
                <!--                        ><o-icon-->
                <!--                            icon="instagram"-->
                <!--                            pack="fab"-->
                <!--                            class="mr-0"-->
                <!--                        ></o-icon-->
                <!--                        >{{ props.row.instagram }}</span-->
                <!--                    >-->
                <!--                </o-table-column>-->
                <o-table-column v-slot="props" label="Actions">
                    <div class="buttons">
                        <o-button
                            icon-left="pencil-alt"
                            variant="warning"
                            @click="
                                $router.push('/app/contacts/' + props.row.id)
                            "
                        >
                            Edit
                        </o-button>

                        <o-button
                            icon-left="trash"
                            variant="info"
                            @click="deleteContact(props.row.id)"
                        >
                            Delete
                        </o-button>
                    </div>
                </o-table-column>
            </o-table>
        </div>

        <div :class="{ 'edit-contacts': true, expanded: selectedId !== null }">
            <ContactsEdit
                v-if="selectedId !== null"
                ref="contactsEdit"
                :contact-id="selectedIdNullIfNew"
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
import { Contact, getFullName } from "@/api/contacts";
import { getAxiosInstance } from "@/api/api";
import { defaultToast } from "@/toasts";
import Spinner from "../components/Spinner.vue";
import ContactsOneToManyList from "@/components/ContactsOneToManyList.vue";
import { debounce, deepCopy } from "@/api/utils";

class Props {
    selectedId: number | null = null;
}

@Options({
    components: { ContactsEdit, Spinner, ContactsOneToManyList },
})
export default class Contacts extends Vue.with(Props) {
    searchQuery = "";
    contacts: Contact[] = [];
    getFullName = getFullName;
    isDiscardChangesDialogActive = false;
    loading = false;
    nextFn: () => void = () => {};

    displayRegularity = (r: number) => {
        if (r === 104) {
            return "Twice a week";
        } else if (r === 52) {
            return "Weekly";
        } else if (r === 26) {
            return "Fortnightly";
        } else if (r === 12) {
            return "Monthly";
        } else if (r === 6) {
            return "Every 2 months";
        } else if (r === 2) {
            return "Twice a year";
        } else if (r === 1) {
            return "Once a year";
        } else if (!r) {
            return null;
        } else {
            return "unknown";
        }
    };

    debounceUpdateSearchQuery = debounce((v: string) => {
        this.searchQuery = v;
    }, 500);

    static NEW_CONTACT = -1;

    get filteredContacts() {
        if (this.searchQuery === "") {
            return this.contacts;
        }
        return this.contacts.filter((c) => {
            return JSON.stringify(c).indexOf(this.searchQuery) !== -1;
        });
    }

    mounted() {
        return Promise.all([this.loadAllContacts()]);
    }

    get selectedIdNullIfNew() {
        if (this.selectedId === Contacts.NEW_CONTACT) {
            return null;
        }
        return this.selectedId;
    }

    hasUnsavedChanges(): boolean {
        return this.$refs.contactsEdit
            ? (this.$refs.contactsEdit as ContactsEdit).hasUnsavedChanges()
            : false;
    }

    async loadAllContacts() {
        this.loading = true;
        let response = await getAxiosInstance().get(
            "contact_book/get_all_contacts"
        );
        this.contacts = response.data;
        this.loading = false;
    }

    openNewContactPane() {
        this.$router.push("/app/contacts/new");
    }

    async deleteContact(id: number) {
        try {
            await getAxiosInstance().delete(
                "contact_book/delete_contact_by_id/" + id
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

    onContactUpdated(contact: Contact) {
        let found = false;
        this.contacts = this.contacts.map((c) => {
            if (c.id === contact.id) {
                found = true;
                return deepCopy(contact);
            } else {
                return c;
            }
        });
        if (!found) {
            this.contacts.push(deepCopy(contact));
        }
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

    beforeWindowUnload(e: BeforeUnloadEvent) {
        if (this.hasUnsavedChanges()) {
            e.preventDefault();
            e.returnValue = "";
        }
    }
}
</script>

<style scoped>
@import "../styles/app-view.css";

.contacts-list {
    flex: 1;
}

.is-full-height {
    height: 100%;
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
