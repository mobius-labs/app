<template>
    <div>
        <ContactsOneToMany
            ref="oneToMany"
            v-slot="{ model, updateItem, debounceUpdateItem }"
            add-button-text="Add Social Media"
            title="Social Media Links"
            :fresh-item="freshSocialMedia"
            api-name="social_media_contact"
            :contact-id="contactId"
            :skip-reload="skipReload"
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

class Props {
    contactId!: number | null;
    // eslint-disable-next-line no-unused-vars
    skipReload!: (a: number | null) => boolean;
}

@Options({
    components: { SocialMediaEditItem, ContactsOneToMany, ValidatedField },
})
export default class SocialMediaEdit extends Vue.with(Props) {
    socialMediaSites = new Map<string, SocialMediaSite>();

    async mounted() {
        let response = await getAxiosInstance().get(
            "/contact_book/get_social_media_sites/"
        );
        this.socialMediaSites.clear();
        for (let site of response.data) {
            this.socialMediaSites.set(site.site, site);
        }
    }

    freshSocialMedia(): Record<string, any> {
        return {};
    }

    hasUnsavedChanges() {
        return (this.$refs.oneToMany as ContactsOneToMany).hasUnsavedChanges();
    }
}
</script>

<style scoped></style>
