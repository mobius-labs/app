<template>
    <div
        class="is-flex"
        style="height: 100%; position: absolute; left: 0; top: 0; width: 100%"
    >
        <div class="is-flex-1 is-flex is-flex-direction-column">
            <div
                class="has-background-black-ter is-flex"
                style="padding: 2rem; margin-bottom: 0"
            >
                <div>
                    <h1 class="title has-text-white-bis">Business Card</h1>
                    <h2 class="subtitle has-text-grey-light">
                        Share business cards online with colleagues in your
                        network.
                    </h2>
                </div>
                <div class="is-flex-grow-1"></div>
                <o-button
                    variant="dark"
                    icon-left="share-square"
                    class="is-large"
                    v-if="user && user.business_card"
                    >Copy link</o-button
                >
            </div>
            <div
                class="
                    is-flex-grow-1
                    is-flex
                    is-flex-direction-column
                    is-align-items-center
                    is-justify-content-center
                    has-background-grey-dark
                "
                style="overflow-y: auto; padding: 5rem 0"
            >
                <BusinessCard :contact="userContact" />

                <transition name="fade">
                    <div v-if="user && userContact" class="has-text-centered">
                        <transition-group name="fade">
                            <div
                                class="edit-button"
                                key="edit"
                                v-if="!isEditingContactDetails"
                            >
                                <a @click="shouldEditContactDetails = true"
                                    ><o-icon icon="pencil-alt"></o-icon> Edit
                                    business card content</a
                                >
                            </div>

                            <o-switch
                                key="enable"
                                v-if="!isEditingContactDetails"
                                size="large"
                                v-model="user.business_card"
                                class="mt-6"
                            >
                                <span class="has-text-grey-lighter">
                                    <span v-if="user.business_card"
                                        >Business card shared</span
                                    >
                                    <span v-else>Business card private</span>
                                </span>
                            </o-switch>
                        </transition-group>
                    </div>
                </transition>
            </div>
        </div>
        <div
            :class="{ 'right-flyout': true, expanded: isEditingContactDetails }"
        >
            <ContactsEdit
                v-if="isEditingContactDetails"
                ref="contactsEdit"
                :local-id="1"
                :server-id="userContact.id"
                :is-business-card="true"
                :is-discard-changes-dialog-active="isDiscardChangesDialogActive"
                @close="shouldEditContactDetails = false"
                @contact-updated="onContactUpdated"
                @discard-changes="discardChanges"
                @cancel-discard="isDiscardChangesDialogActive = false"
            >
                <div class="content">
                    <p>
                        If you select to share your business card, then anyone
                        with the link will be able to view the contact details
                        you've entered.
                    </p>
                </div>

                <o-switch v-model="user.business_card">
                    <span v-if="user.business_card">Business card shared</span>
                    <span v-else>Business card private</span>
                </o-switch>

                <hr />
            </ContactsEdit>
        </div>
    </div>
</template>

<script lang="ts">
import BusinessCard from "@/components/BusinessCard.vue";
import { Contact } from "@/api/contacts";
import ContactsEdit from "@/components/ContactsEdit.vue";
import { defineComponent } from "vue";
import { getAxiosInstance } from "@/api/api";
import { fetchUserDetails, User } from "@/api/user";

export default defineComponent({
    name: "BusinessCardEdit",
    components: { BusinessCard, ContactsEdit },
    data() {
        return {
            shouldEditContactDetails: false,
            userContact: null as Contact | null,
            isDiscardChangesDialogActive: false,
            user: null as User | null,
        };
    },
    computed: {
        isEditingContactDetails() {
            // TODO: work out why this doesn't work
            return (
                (this as any).shouldEditContactDetails &&
                (this as any).userContact
            );
        },
    },
    watch: {
        "user.business_card": "putUserDetails",
    },
    mounted() {
        this.fetchUserDetails();
        this.fetchUserContact();
    },
    methods: {
        async fetchUserDetails() {
            this.user = await fetchUserDetails();
        },
        async fetchUserContact() {
            try {
                const result = await getAxiosInstance().get(
                    "/contact_book/get_user_contacts"
                );
                this.userContact = result.data as Contact;
            } catch (e) {
                this.userContact = null;
            }
        },
        async putUserDetails() {
            try {
                const result = await getAxiosInstance().put(
                    "/account/update_business_card_visibility",
                    this.user
                );
                console.log(result);
            } catch (e) {
                console.error(e);
            }
        },
        async onContactUpdated() {
            await this.fetchUserContact();
        },

        // eslint-disable-next-line @typescript-eslint/no-empty-function
        discardChanges() {},
    },
});
</script>

<style scoped lang="scss">
@import "../styles/flyout.css";
@import "../styles/variables";

.is-flex-1 {
    flex: 1;
}

.edit-button {
    margin-top: 1.5rem;

    a:hover {
        color: lighten($link, 10%);
    }
}
</style>
