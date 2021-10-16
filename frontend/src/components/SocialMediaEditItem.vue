<template>
    <div class="is-flex is-flex-grow-1 is-align-items-center mb-1">
        <ValidatedField
            v-slot="{ value, setValue }"
            :label="null"
            :model="model"
            name="social_media_site"
            :update-value="updateItem"
            class="mb-0"
        >
            <o-dropdown>
                <template #trigger>
                    <o-tooltip
                        label="Click to choose a different site"
                        position="right"
                    >
                        <o-button size="medium" variant="text">
                            <o-icon
                                v-if="value"
                                :icon="
                                    socialMediaSites.get(value)?.icon || 'link'
                                "
                                :pack="
                                    socialMediaSites.get(value)?.icon !== ''
                                        ? 'fab'
                                        : 'fas'
                                "
                            ></o-icon>
                            <span v-else>Select social media site</span>
                        </o-button>
                    </o-tooltip>
                </template>
                <o-dropdown-item
                    v-for="site in socialMediaSites.values()"
                    :key="site.site"
                    :value="site.site"
                    @click="setValue(site.site)"
                >
                    <o-icon
                        :icon="site.icon || 'link'"
                        :pack="site.icon !== '' ? 'fab' : 'fas'"
                    ></o-icon>
                    {{ site.site }}
                </o-dropdown-item>
                <o-dropdown-item v-if="socialMediaSites.size === 0"
                    >No items</o-dropdown-item
                >
            </o-dropdown>
        </ValidatedField>
        <ValidatedField
            v-slot="{ value }"
            :model="model"
            name="link"
            :label="null"
            class="is-flex-grow-1"
            :update-value="(v) => recognizeSiteAndUpdateItem(v)"
            required
        >
            <o-tooltip
                v-if="editingLink"
                label="Enter a username or paste profile URL"
            >
                <o-input
                    :model-value="value"
                    placeholder="Enter username or paste URL"
                    @keyup.enter="submit"
                    @update:model-value="(v) => (newLinkValue = v)"
                />
            </o-tooltip>
            <a
                v-else
                :href="computedLink"
                target="_blank"
                class="has-text-primary"
                style="margin-top: 0.125rem"
                >{{ computedLink }}</a
            >
            <o-button v-if="editingLink" variant="primary" @click="submit"
                >Done</o-button
            >
            <button
                v-else
                class="button is-text is-rounded is-small ml-2"
                style="text-decoration: none"
            >
                <o-icon
                    size="small"
                    icon="pencil-alt"
                    class="has-text-grey"
                    @click="editLink"
                ></o-icon>
            </button>
        </ValidatedField>
    </div>
</template>

<script lang="ts">
import { Options, Vue, prop } from "vue-class-component";
import ValidatedField from "@/components/ValidatedField.vue";
import {
    formatSocialLink,
    Recognition,
    SocialMediaSite,
    tryRecogniseSocialLink,
} from "@/api/social";
import { PropType } from "vue";
import { Model } from "@/api/model";

class Props {
    model!: Model;
    updateItem!: (v: Record<string, any>) => void;
    socialMediaSites = prop({
        type: Object as PropType<Map<string, SocialMediaSite>>,
        required: true,
    });
}

@Options({
    components: { ValidatedField },
})
export default class SocialMediaEditItem extends Vue.with(Props) {
    shouldEditLink = false;
    newLinkValue = "";

    get editingLink() {
        return (
            !this.model.model.social_media_site ||
            !this.model.model.link ||
            this.shouldEditLink
        );
    }

    get computedLink() {
        const site = this.socialMediaSites.get(
            this.model.model.social_media_site
        );
        if (!site) {
            return null;
        }
        return formatSocialLink(site, this.model.model.link);
    }

    editLink() {
        this.newLinkValue = this.model.model.link;
        this.shouldEditLink = true;
    }

    // When submitting a link/username, we try to autodetect which social media site it is for,
    // and set the info accordingly.
    submit() {
        const recognition: Recognition | null = tryRecogniseSocialLink(
            this.socialMediaSites,
            this.newLinkValue
        );
        if (recognition !== null) {
            this.updateItem({
                social_media_site: recognition.site.site,
                link: recognition.username,
            });
        } else {
            this.updateItem({ link: this.newLinkValue });
        }
        this.shouldEditLink = false;
    }
}
</script>

<style scoped></style>
