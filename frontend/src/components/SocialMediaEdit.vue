<template>
    <div>
        <ContactsOneToMany
            ref="oneToMany"
            v-slot="{ model, updateItem }"
            add-button-text="Add Social Media"
            title="Social Media Links"
            :fresh-item="freshSocialMedia"
            api-name="social_media_contact"
            :initial-items="initialItems"
            :server-id="serverId"
            @update:saving="(a, v) => $emit('update:saving', a, v)"
            @update:recently-updated="
                (a, v) => $emit('update:recently-updated', a, v)
            "
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
import { ServerContactId, SocialMedia } from "@/api/contacts";

class Props {
    initialItems!: SocialMedia[];
    serverId!: ServerContactId;
}

// A specialized version of ContactsOneToMany, for editing SocialMediaContacts
@Options({
    components: { SocialMediaEditItem, ContactsOneToMany, ValidatedField },
    emits: ["update:saving", "update:recently-updated"],
})
export default class SocialMediaEdit extends Vue.with(Props) {
    socialMediaSites = new Map<string, SocialMediaSite>();

    async mounted() {
        this.socialMediaSites = await getSocialMediaSites();
    }

    freshSocialMedia(): Record<string, any> {
        return { social_media_site: "Other" };
    }

    hasUnsavedChanges() {
        return (
            this.$refs.oneToMany as typeof ContactsOneToMany
        ).hasUnsavedChanges();
    }
}
</script>

<style scoped></style>
