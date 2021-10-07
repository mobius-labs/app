<template>
    <div class="is-flex is-align-items-stretch is-full-height">
        <div class="contacts-list">
            <div class="app-header">
                <h1 class="title">Contacts</h1>
                <div class="ml-6 mr-4">
                    <o-input
                        class=""
                        type="search"
                        icon="search"
                        placeholder="Search for contacts..."
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

            <o-table hoverable focusable :data="contacts">
                <o-table-column v-slot="props" label="Name">
                    {{ getFullName(props.row) }}
                </o-table-column>
                <o-table-column v-slot="props" label="Contacts">
                    <span v-if="props.row.email" class="tag mr-2"
                        ><o-icon icon="envelope" class="mr-0" />{{
                            props.row.email
                        }}</span
                    >
                    <span v-if="props.row.phone" class="tag mr-2"
                        ><o-icon icon="phone" class="mr-0" />{{
                            props.row.phone
                        }}</span
                    >
                </o-table-column>
                <o-table-column v-slot="props" label="Address">
                    {{ props.row.address }}
                </o-table-column>
                <o-table-column
                    v-if="selectedId === null"
                    v-slot="props"
                    label="Last Contacted"
                >
                    {{ props.row.lastContacted }}
                </o-table-column>
                <o-table-column
                    v-if="selectedId === null"
                    v-slot="props"
                    label="Social Media"
                >
                    <span v-if="props.row.facebook" class="tag is-link"
                        ><o-icon
                            icon="facebook"
                            pack="fab"
                            class="mr-0"
                        ></o-icon
                        >{{ props.row.facebook }}</span
                    >
                    <span v-if="props.row.instagram" class="tag is-link"
                        ><o-icon
                            icon="instagram"
                            pack="fab"
                            class="mr-0"
                        ></o-icon
                        >{{ props.row.instagram }}</span
                    >
                </o-table-column>
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

        <ContactsEdit
            ref="contactsEdit"
            :expanded="selectedId !== null"
            :contact="selectedContact"
            :is-discard-changes-dialog-active="isDiscardChangesDialogActive"
            @refresh-contacts="loadAllContacts"
            @discard-changes="discardChanges"
            @cancel-discard="isDiscardChangesDialogActive = false"
        />
    </div>
</template>

<script lang="ts">
import ContactsEdit from "../components/ContactsEdit.vue";
import { Options, Vue } from "vue-class-component";
import { Contact, getFullName } from "@/api/contacts";
import { getAxiosInstance } from "@/api/api";
import { defaultToast } from "@/toasts";

class Props {
    selectedId: number | null = null;
}

@Options({
    components: { ContactsEdit },
    watch: { selectedId: "loadSelectedContact" },
})
export default class Contacts extends Vue.with(Props) {
    contacts: Contact[] = [];
    getFullName = getFullName;
    selectedContact: Contact | null = null;
    isDiscardChangesDialogActive = false;
    nextFn: () => void = () => {};

    static NEW_CONTACT = -1;

    mounted() {
        return Promise.all([
            this.loadAllContacts(),
            this.loadSelectedContact(),
        ]);
    }

    async loadAllContacts() {
        let response = await getAxiosInstance().get(
            "contact_book/get_all_contacts"
        );
        this.contacts = response.data;
    }

    async loadSelectedContact() {
        if (this.selectedId === null) {
            this.selectedContact = null;
        } else if (this.selectedId === Contacts.NEW_CONTACT) {
            this.selectedContact = new Contact();
        } else {
            let matchingContacts = this.contacts.filter(
                (c) => c.id == this.selectedId
            );
            if (matchingContacts.length > 0) {
                this.selectedContact = matchingContacts[0];
            } else {
                this.selectedContact = null;
                let response = await getAxiosInstance().get(
                    "contact_book/get_contact_by_id/" + this.selectedId
                );
                this.selectedContact = response.data;
            }
        }
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

    checkForUnsavedChanges(next: () => void) {
        let unsaved = (
            this.$refs.contactsEdit as ContactsEdit
        ).hasUnsavedChanges();
        console.log("beforeRouteUpdate", unsaved);
        if (unsaved) {
            this.isDiscardChangesDialogActive = true;
            this.nextFn = next;
        } else {
            next();
        }
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
</style>
