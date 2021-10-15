<template>
    <Navbar />
    <div
        class="
            has-background-info
            is-flex
            is-flex-direction-column
            is-align-items-center
            is-justify-content-center
        "
        style="height: 100%"
    >
        <BusinessCard :contact="contact"></BusinessCard>
        <div v-if="contact" class="mt-6 pt-6 has-text-centered">
            <h2
                class="title"
                style="font-weight: 100"
                v-if="authenticated === true"
            >
                {{ contact.first_name }} is also on Möbius
            </h2>
            <o-button
                class="is-medium"
                variant="primary"
                v-if="authenticated === true"
                icon-left="plus-circle"
                >Add to your contacts</o-button
            >
            <h2
                class="subtitle"
                style="font-weight: 400; max-width: 30rem"
                v-if="authenticated === false"
            >
                Möbius helps you manage your connections, maintain your
                relationships, and never miss a date!
            </h2>
            <o-button
                tag="router-link"
                to="/signup"
                class="is-medium"
                variant="primary"
                v-if="authenticated === false"
                >Join Möbius for free</o-button
            >
        </div>
    </div>
</template>

<script lang="ts">
import BusinessCard from "@/components/BusinessCard.vue";
import { defineComponent } from "vue";
import { getAxiosInstance } from "@/api/api";
import { FullContact, getFullName } from "@/api/contacts";
import Navbar from "@/components/Navbar.vue";

export default defineComponent({
    name: "BusinessCardView",
    components: { BusinessCard, Navbar },
    props: {
        email: { type: String, required: true },
    },
    data() {
        return {
            contact: null as FullContact | null,
            authenticated: null as boolean | null,
            fullName: getFullName,
        };
    },
    async mounted() {
        return Promise.all([this.determineAuthStatus(), this.loadContact()]);
    },
    methods: {
        async determineAuthStatus() {
            this.authenticated = await this.$store.dispatch(
                "determineAuthStatus"
            );
        },
        async loadContact() {
            const result = await getAxiosInstance().get(
                "/contact_book/get_business_cards/" + this.email
            );
            console.log(result);
            this.contact = result.data as FullContact;
            document.title = this.contact.first_name + "'s business card";
        },
    },
});
</script>

<style scoped></style>
