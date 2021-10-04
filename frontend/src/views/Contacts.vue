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
            </div>

            <o-table
                hoverable
                focusable
                :data="fakeContacts"
                :v-model:selected="selected"
            >
                <o-table-column v-slot="props" label="Name">
                    {{ props.row.name }}
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

// this data doesn't represent what will be returned by the API, instead,
// it is super simplified just for displaying in this mockup
const fakeContacts = [
    {
        name: "James McAlfey",
        email: "james@gmail.com",
        address: "93 Foobar St",
        phone: "9888 2932",
        lastContacted: "6 months ago",
        facebook: "james.mcalfey",
    },
    {
        name: "Foo Bar",
        email: "james@yahoo.com",
        address: "93 Foobar St",
        phone: "9234 2932",
        lastContacted: "yesterday",
        instagram: "foo.bar",
    },
];

export default {
    name: "Contacts",
    components: { ContactsEdit },
    data() {
        return {
            fakeContacts: fakeContacts,
            selected: null,
        };
    },
};
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
