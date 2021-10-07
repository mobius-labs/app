<template>
    <div>
        <slot v-for="item of items" :item="item"></slot>
    </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getAxiosInstance } from "@/api/api";

class Props {
    contactId!: number | null;
    apiName!: string;
}

@Options({
    watch: { contactId: "fetchAllItems" },
})
export default class ContactsOneToManyList extends Vue.with(Props) {
    items = [];

    async mounted() {
        await this.fetchAllItems();
    }

    async fetchAllItems() {
        let response = await getAxiosInstance().get(
            "/contact_book/get_" + this.apiName + "s_by_cid/" + this.contactId
        );
        this.items = response.data;
    }
}
</script>

<style scoped></style>
