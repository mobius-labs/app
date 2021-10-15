<template>
    <div class="bc-wrapper has-text-left">
        <div :class="'bc bc-theme-' + theme">
            <div class="bc-photo">
                <transition name="fade" mode="out-in">
                    <UserIcon
                        v-if="!contact || primaryEmail"
                        :user="primaryEmail ? { email: primaryEmail } : null"
                        :class="{
                            'bc-icon': true,
                            'bc-icon-loading': !gravatarLoaded,
                        }"
                        v-model:loaded="gravatarLoaded"
                    >
                        <template #fallback>
                            <o-skeleton
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
        theme: { type: String, default: "default" },
    },
    data() {
        return {
            fullName: getFullName,
            concatAddress: concatAddress,
            socialMediaSites: new Map(),
            gravatarLoaded: false,
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
}

is-centered {
    align-items: center;
}

@keyframes popOut {
    50% {
        transform: scale(1.02);
    }
}

.bc {
    transition: box-shadow 0.2s ease, border 0.2s ease;
    //border: 10px solid transparent;
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
    margin-bottom: 1rem;
}

.bc-icon {
    width: 6rem;
    height: 6rem;
    border: 2px solid $grey-dark;
    transition: border-color 0.2s ease;
    border-radius: 50%;
    overflow: hidden;

    &.bc-icon-loading {
        border-color: transparent;
    }
}

.bc-name-title-details {
    display: flex;
}

.bc-name-title {
    flex: 1;
    text-align: right;
}

.bc-name {
    margin-bottom: 0;
}

.bc-title {
    font-style: italic;
}

.bc hr {
    margin-top: 1rem;
    margin-bottom: 1rem;
    height: 1px;
    width: 70%;
    margin-left: auto;
    background-color: $grey;
}

.bc-contact-details {
    margin-left: 20px;
    flex: 1;
}

.bc-item {
}

.bc-theme-default {
    font-family: "Source Sans Pro", sans-serif;
    font-size: 14px;
    background-image: radial-gradient(
        circle farthest-corner at 18.7% 37.8%,
        rgba(250, 250, 250, 1) 0%,
        rgba(225, 234, 238, 1) 90%
    );
    border-radius: 0.5rem;
    padding: 2rem;
}
</style>
