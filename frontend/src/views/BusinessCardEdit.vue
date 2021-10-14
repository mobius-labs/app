<template>
    <div class="is-flex" style="height: 100%">
        <div class="is-flex-1 is-flex is-flex-direction-column">
            <div class="level" style="padding: 2rem">
                <div>
                    <h1 class="title">Business Card</h1>
                    <h2 class="subtitle">
                        Share business cards online with colleagues in your
                        network.
                    </h2>
                </div>
            </div>
            <div
                class="
                    is-flex-grow-1
                    is-flex
                    is-flex-direction-column
                    is-align-items-center
                    is-justify-content-center
                    has-background-grey-lighter
                "
            >
                <transition name="fade">
                    <div v-if="user && userContact" class="has-text-centered">
                        <BusinessCard :contact="userContact" />
                        <o-switch
                            size="large"
                            v-model="user.business_card"
                            class="mt-6"
                        >
                            <span v-if="user.business_card"
                                >Business card shared</span
                            >
                            <span v-else>Business card not shared</span>
                        </o-switch>
                    </div>
                </transition>
                <o-button @click="shouldEditContactDetails = true"
                    >Edit</o-button
                >
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
            />
        </div>
    </div>
</template>

<script lang="ts">
import BusinessCard from "@/components/BusinessCard.vue";
import { Contact, ContactId, ServerContactId } from "@/api/contacts";
import ContactsEdit from "@/components/ContactsEdit.vue";
import { defineComponent } from "vue";
import { getAxiosInstance } from "@/api/api";

interface User {
    email: string;
    business_card: boolean;
}

export default defineComponent({
    name: "BusinessCardEdit",
    components: { BusinessCard, ContactsEdit },
    data() {
        return {
            shouldEditContactDetails: false,
            isDiscardChangesDialogActive: false,
            userContact: null as Contact | null,
            user: null as User | null,
        };
    },
    watch: {
        "user.business_card": "putUserDetails",
    },
    mounted() {
        this.fetchUserDetails();
        this.fetchUserContact();
    },
    computed: {
        isEditingContactDetails() {
            return this.shouldEditContactDetails && this.userContact;
        },
    },
    methods: {
        async fetchUserDetails() {
            const result = await getAxiosInstance().get(
                "/account/get_business_card_visibility"
            );
            this.user = result.data as User;
        },
        async fetchUserContact() {
            const result = await getAxiosInstance().get(
                "/contact_book/get_user_contacts"
            );
            this.userContact = result.data as Contact;
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
        async onContactUpdated(
            localId: ContactId,
            serverId: ServerContactId,
            newlyCreated: boolean
        ) {
            await this.fetchUserContact();
            console.log(localId, serverId, newlyCreated);
        },

        // eslint-disable-next-line @typescript-eslint/no-empty-function
        discardChanges() {},
    },
});
</script>

<style scoped>
@import "../styles/flyout.css";

.is-flex-1 {
    flex: 1;
}
</style>
