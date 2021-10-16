<template>
    <div>
        <o-icon :icon="icon || 'link'" :pack="icon ? 'fab' : 'fas'"></o-icon>
        <a :href="computedLink" target="_blank" style="margin-top: 0.125rem">{{
            item.link
        }}</a>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { formatSocialLink, SocialMediaSite } from "@/api/social";

export default defineComponent({
    name: "SocialMediaItem",
    props: {
        socialMediaSites: {
            type: Object as PropType<Map<string, SocialMediaSite>>,
            required: true,
        },
        item: { type: Object, required: true },
    },
    computed: {
        icon() {
            return this.socialMediaSites.get(this.item.social_media_site)?.icon;
        },
        computedLink() {
            const site = this.socialMediaSites.get(this.item.social_media_site);
            if (!site) {
                return null;
            }
            return formatSocialLink(site, this.item.link);
        },
    },
});
</script>

<style scoped></style>
