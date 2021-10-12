<template>
    <transition name="fade" mode="out-in">
        <div v-if="fetched">
            <slot v-for="item of items" :item="item"></slot>
        </div>
        <div v-else>...</div>
    </transition>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { getAxiosInstance } from "@/api/api";

class Props {
    contactId!: number | null;
    version!: number;
    apiName!: string;
}

@Options({
    watch: { contactId: "fetchAllItems", version: "fetchAllItems" },
})
export default class ContactsOneToManyList extends Vue.with(Props) {
    items = [];
    fetched = false;
    observer: IntersectionObserver | null = null;

    created() {
        // we use this the IntersectionObserver API to only
        // make API requests for this element once it is visible on the user's screen.
        this.observer = new IntersectionObserver(this.onIntersectionObserved, {
            threshold: 0.1,
        });
    }

    mounted() {
        this.observer?.observe(this.$el);
    }

    beforeDestroy() {
        this.observer?.disconnect();
    }

    async onIntersectionObserved(entries: IntersectionObserverEntry[]) {
        for (let entry of entries) {
            if (!entry.isIntersecting) {
                return;
            }
            this.observer?.unobserve(entry.target);
            if (!this.fetched) {
                await this.fetchAllItems();
                this.fetched = true;
            }
        }
    }

    async fetchAllItems() {
        if (!this.contactId) {
            return;
        }
        console.log("fetching", this.contactId);
        let response = await getAxiosInstance().get(
            "/contact_book/get_" + this.apiName + "s_by_cid/" + this.contactId
        );
        this.items = response.data;
    }
}
</script>

<style scoped></style>
