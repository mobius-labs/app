<template>
    <div>
        <ContactsOneToMany
            ref="oneToMany"
            v-slot="{ model, updateItem, debounceUpdateItem }"
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
                :debounce-update-item="debounceUpdateItem"
                :social-media-sites="socialMediaSites"
            ></SocialMediaEditItem>
        </ContactsOneToMany>
    </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import ContactsOneToMany from "@/components/ContactsOneToMany.vue";
import { getAxiosInstance } from "@/api/api";
import ValidatedField from "@/components/ValidatedField.vue";
import SocialMediaEditItem from "@/components/SocialMediaEditItem.vue";
import { SocialMediaSite } from "@/api/social";
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
        const response = await getAxiosInstance().get(
            "/contact_book/get_social_media_sites/"
        );
        this.socialMediaSites.clear();
        for (const site of response.data as SocialMediaSite[]) {
            this.socialMediaSites.set(site.site, site);
        }
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
