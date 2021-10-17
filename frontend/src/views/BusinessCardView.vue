<template>
    <Navbar />
    <div
        class="
            is-flex
            is-flex-direction-column
            is-align-items-center
            is-justify-content-center
            scroll-container
        "
    >
        <div v-if="loadingFailed" class="has-text-centered">
            <h2 class="subtitle">
                We're sorry but we couldn't find a business card here!
            </h2>
            <p>
                This user either doesn't exist, or has chosen to keep their
                business card private.
            </p>
            <o-button tag="router-link" to="/" class="mt-6"
                >Back to Homepage</o-button
            >
        </div>
        <BusinessCard
            v-else
            :contact="contact"
            :theme="derivedTheme"
        ></BusinessCard>
        <div
            v-if="contact"
            class="mt-6 pt-6 has-text-centered"
            style="max-width: 30rem"
        >
            <div v-if="isUsersOwnContact === true">
                <h2 class="subtitle" style="font-weight: 100">
                    This is how your business card will look when shared with
                    others.
                </h2>
                <o-button
                    tag="router-link"
                    to="/app/business-card"
                    class="is-medium"
                    variant="primary"
                    icon-left="pencil-alt"
                    >Edit Business Card</o-button
                >
            </div>
            <div v-else-if="isUsersOwnContact === false">
                <h2 class="title" style="font-weight: 100">
                    {{ contact.first_name }} is also on Möbius
                </h2>
                <o-button
                    class="is-medium"
                    variant="primary"
                    icon-left="plus-circle"
                    @click="addToContacts"
                    >Add to your contacts</o-button
                >
            </div>
            <div v-else-if="authenticated === false">
                <h1 class="title" style="font-weight: 100">
                    {{ contact.first_name }} is on Möbius
                </h1>
                <h2 class="subtitle mt-3" style="font-weight: 100">
                    Möbius helps you manage your connections, maintain your
                    relationships, and never miss a date!
                </h2>
                <o-button
                    tag="router-link"
                    to="/signup"
                    class="is-medium"
                    variant="primary"
                    >Join Möbius for free</o-button
                >
            </div>
        </div>
    </div>
</template>

<script>
import BusinessCard from "@/components/BusinessCard.vue";
import { getAxiosInstance } from "@/api/api";
import { getFullName, stripIdsFromContact } from "@/api/contacts";
import Navbar from "@/components/Navbar.vue";
import { getTheme } from "@/businessCard";
import { fetchUserDetails } from "@/api/user";

export default {
    name: "BusinessCardView",
    components: { BusinessCard, Navbar },
    props: {
        email: { type: String, required: true },
    },
    data() {
        return {
            contact: null,
            theme: null,
            user: null,
            authenticated: null,
            fullName: getFullName,
            loadingFailed: false,
        };
    },
    computed: {
        isUsersOwnContact() {
            if (!this.user) {
                return null;
            }
            return this.email === this.user.email;
        },
        derivedTheme() {
            return getTheme({ business_card_theme: this.theme });
        },
    },
    async mounted() {
        await this.determineAuthStatus();
        await this.loadContact();
    },
    methods: {
        async determineAuthStatus() {
            this.authenticated = await this.$store.dispatch(
                "determineAuthStatus"
            );
            if (this.authenticated) {
                this.user = await fetchUserDetails();
            }
        },
        async loadContact() {
            try {
                const result = await getAxiosInstance().get(
                    "/contact_book/get_business_cards/" + this.email
                );
                this.theme = result.data.business_card_theme;
                delete result.data.business_card_theme;
                this.contact = result.data;
                document.title = this.contact.first_name + "'s business card";
            } catch (e) {
                this.loadingFailed = true;
            }
        },
        addToContacts() {
            const stripped = stripIdsFromContact(this.contact);

            this.$router.push({
                path: "/app/contacts",
                query: {
                    initialData: JSON.stringify(stripped),
                },
            });
        },
    },
};
</script>

<style scoped lang="scss">
.scroll-container {
    height: 100%;
    overflow-y: auto;
    padding: 4rem 0 8rem 0;

    @media screen and (max-width: 50rem) {
        justify-content: flex-start;
    }
}
</style>
