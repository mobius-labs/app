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
                    @click="openNewContactPane"
                    >Add Contact</o-button
                >
            </div>

            <o-table
                hoverable
                focusable
                :data="contacts"
                :v-model:selected="selected"
            >
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
                    v-if="selected === null"
                    v-slot="props"
                    label="Last Contacted"
                >
                    {{ props.row.lastContacted }}
                </o-table-column>
                <o-table-column
                    v-if="selected === null"
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
                    <o-button
                        icon-left="pencil-alt"
                        variant="warning"
                        @click="selected = props.row"
                    >
                        Edit
                    </o-button>
                </o-table-column>
            </o-table>
        </div>

        <ContactsEdit
            :expanded="selected !== null"
            :contact="selected"
            @close="selected = null"
        />
    </div>
</template>

<script lang="ts">
import ContactsEdit from "../components/ContactsEdit.vue";
import { Options, Vue } from "vue-class-component";
import { Contact, getFullName } from "@/api/contacts";
import { getAxiosInstance } from "@/api/api";

@Options({
    components: { ContactsEdit },
})
export default class Contacts extends Vue {
    contacts = [];
    selected: Contact | null = null;
    getFullName = getFullName;

    async mounted() {
        let response = await getAxiosInstance().get(
            "contact_book/get_all_contacts"
        );
        console.log(response);
        this.contacts = response.data;
    }

    openNewContactPane() {
        this.selected = new Contact();
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
