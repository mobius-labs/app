<template>
    <div class="bc-wrapper has-text-left">
        <div :class="'bc bc-theme-' + theme">
            <div class="bc-photo">
                <transition name="fade" mode="out-in">
                    <UserIcon
                        :user="primaryEmail ? { email: primaryEmail } : null"
                        class="bc-icon"
                    >
                        <template #loading>
                            <o-skeleton
                                key="loading"
                                animated
                                circle
                                width="6rem"
                                height="6rem"
                            ></o-skeleton>
                        </template>
                    </UserIcon>
                </transition>
            </div>
            <div class="bc-name-title-details">
                <div class="bc-name-title">
                    <transition name="fade" mode="out-in">
                        <h2 class="subtitle bc-name" v-if="contact">
                            {{ fullName(contact) }}
                            <span v-if="contact.pronouns"
                                >({{ contact.pronouns }})</span
                            >
                        </h2>
                        <o-skeleton v-else animated height="2rem"></o-skeleton>
                    </transition>
                    <hr />
                    <transition name="fade" mode="out-in">
                        <p class="bc-title" v-if="contact && contact.job_title">
                            {{ contact.job_title
                            }}<span v-if="contact.company"
                                >, {{ contact.company }}</span
                            >
                        </p>
                        <p
                            class="bc-title"
                            v-else-if="contact && !contact.job_title"
                        >
                            <em class="bc-placeholder">[Job Title]</em>
                        </p>
                        <o-skeleton v-else-if="!contact" animated></o-skeleton>
                    </transition>
                </div>
                <div class="bc-contact-details">
                    <transition name="fade" mode="out-in">
                        <div v-if="contact">
                            <div
                                v-for="item in contact.phone_nos"
                                :key="item.id"
                                class="bc-item bc-phone-item"
                            >
                                <o-icon icon="phone"></o-icon>{{ item.number }}
                            </div>
                            <div
                                v-for="item in contact.emails"
                                :key="item.id"
                                class="bc-item bc-email-item"
                            >
                                <o-icon icon="envelope"></o-icon
                                ><a :href="'mailto:' + item.email_address">{{
                                    item.email_address
                                }}</a>
                            </div>
                            <div
                                v-for="item in contact.social_media"
                                :key="item.id"
                                class="bc-item bc-social-item"
                            >
                                <SocialMediaItem
                                    :social-media-sites="socialMediaSites"
                                    :item="item"
                                ></SocialMediaItem>
                            </div>
                            <div
                                v-for="item in contact.addresses"
                                :key="item.id"
                                class="bc-item bc-address-item"
                            >
                                <o-icon icon="map-marker-alt"></o-icon
                                >{{ concatAddress(item) }}
                            </div>
                        </div>
                        <o-skeleton
                            v-else-if="!contact"
                            animated
                            :count="5"
                        ></o-skeleton>
                    </transition>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { getFullName, concatAddress, FullContact } from "@/api/contacts";
import { getSocialMediaSites } from "@/api/social";
import SocialMediaItem from "@/components/SocialMediaItem.vue";
import UserIcon from "@/components/UserIcon.vue";

export default defineComponent({
    name: "BusinessCard",
    components: { UserIcon, SocialMediaItem },
    props: {
        contact: { type: Object as PropType<FullContact>, default: null },
        theme: { type: String, required: true },
    },
    data() {
        return {
            fullName: getFullName,
            concatAddress: concatAddress,
            socialMediaSites: new Map(),
        };
    },
    computed: {
        primaryEmail() {
            // return 'foo';
            if (this.contact && this.contact.emails.length > 0) {
                return this.contact.emails[0].email_address;
            }
            return null;
        },
    },
    async mounted() {
        this.socialMediaSites = await getSocialMediaSites();
    },
});
</script>

<style scoped lang="scss">
@import "../styles/variables";
.bc-wrapper {
    width: 30rem;

    @media screen and (max-width: 35rem) {
        width: auto !important;
    }
}

.is-centered {
    align-items: center;
}

@keyframes popOut {
    50% {
        transform: scale(1.02);
    }
}

.bc {
    transition: box-shadow 0.2s ease, border 0.2s ease;
    padding: 2em;
    border-radius: 0.5em;
    font-size: 0.8em;
}

.bc:hover,
.bc:focus,
.bc:active {
    animation-name: popOut;
    animation-duration: 0.5s;
    animation-timing-function: linear;
    animation-iteration-count: 1;
    //border-color: #fff;
    //box-shadow: 0 0 10px 0px #000;
}

.bc-photo {
    display: flex;
    justify-content: center;
    margin-bottom: 1em;
}

.bc-icon {
    width: 8em;
    height: 8em;
    transition: border-color 0.2s ease;
    overflow: hidden;

    :deep(img) {
        border: 2px solid $grey-dark;
        border-radius: 50%;
    }
}

.bc-name-title-details {
    display: flex;
}

.bc-name-title {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: right;
}

.bc-name {
    margin-bottom: 0 !important;
}

.bc-title {
    font-style: italic;
}

.bc hr {
    margin-top: 1em;
    margin-bottom: 1em;
    height: 1px;
    width: 70%;
    margin-left: auto;
    background-color: $grey;
}

.bc-contact-details {
    margin-left: 2em;
    flex: 1;
}

.bc-placeholder {
    color: $grey;
}

.bc-item {
}
</style>
<style lang="scss">
@import "../styles/businessCardThemes";
</style>
