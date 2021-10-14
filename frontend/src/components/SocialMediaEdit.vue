<template>
    <div>
        <ContactsOneToMany
            ref="oneToMany"
            v-slot="{ model, updateItem }"
            add-button-text="Add Social Media"
            title="Social Media Links"
            :fresh-item="freshSocialMedia"
            api-name="social_media_contact"
            :local-id="localId"
            :server-id="serverId"
            @update:saving="(v) => $emit('update:saving', v)"
        >
            <SocialMediaEditItem
                :model="model"
                :update-item="updateItem"
                :social-media-sites="socialMediaSites"
            ></SocialMediaEditItem>
        </ContactsOneToMany>
    </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import ContactsOneToMany from "@/components/ContactsOneToMany.vue";
import ValidatedField from "@/components/ValidatedField.vue";
import SocialMediaEditItem from "@/components/SocialMediaEditItem.vue";
import { getSocialMediaSites, SocialMediaSite } from "@/api/social";
import { ContactId, ServerContactId } from "@/api/contacts";

class Props {
    localId!: ContactId;
    serverId!: ServerContactId;
}

// A specialized version of ContactsOneToMany, for editing SocialMediaContacts
@Options({
    components: { SocialMediaEditItem, ContactsOneToMany, ValidatedField },
})
export default class SocialMediaEdit extends Vue.with(Props) {
    socialMediaSites = new Map<string, SocialMediaSite>();

    async mounted() {
        this.socialMediaSites = await getSocialMediaSites();
    }

    freshSocialMedia(): Record<string, any> {
        return {};
    }

    hasUnsavedChanges() {
        return (
            this.$refs.oneToMany as typeof ContactsOneToMany
        ).hasUnsavedChanges();
    }
}
</script>

<style scoped></style>
