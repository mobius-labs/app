<template>
    <div class="is-flex" style="height: 100%">
        <div class="is-flex-1">
            <div class="level" style="padding: 2rem">
                <div>
                    <h1 class="title">Business Card</h1>
                    <h2 class="subtitle">
                        Share business cards online with colleagues in your
                        network.
                    </h2>
                </div>
            </div>
            <div>
                <div>
                    <BusinessCard :contact="{}" />
                </div>
                <o-switch size="large">Business card shared</o-switch>
                <o-button @click="isEditingContactDetails = true"
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
                :server-id="contactId"
                :is-discard-changes-dialog-active="isDiscardChangesDialogActive"
                @close="isEditingContactDetails = false"
                @contact-updated="onContactUpdated"
                @discard-changes="discardChanges"
                @cancel-discard="isDiscardChangesDialogActive = false"
            />
        </div>
    </div>
</template>

<script lang="ts">
import BusinessCard from "@/components/BusinessCard.vue";
import { ContactId, ServerContactId } from "@/api/contacts";
import ContactsEdit from "@/components/ContactsEdit.vue";
import { defineComponent } from "vue";

export default defineComponent({
    name: "BusinessCardEdit",
    components: { BusinessCard, ContactsEdit },
    data() {
        return {
            isEditingContactDetails: false,
            contactId: null,
        };
    },
    methods: {
        async onContactUpdated(
            localId: ContactId,
            serverId: ServerContactId,
            newlyCreated: boolean
        ) {
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
