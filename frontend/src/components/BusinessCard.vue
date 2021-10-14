<template>
    <div class="bc-wrapper has-text-left">
        <div :class="'bc bc-theme-' + theme">
            <div class="bc-photo">
                <UserIcon
                    :user="primaryEmail ? { email: primaryEmail } : null"
                    :fallback="false"
                ></UserIcon>
            </div>
            <div class="bc-name-title-details">
                <div class="bc-name-title">
                    <h2 class="subtitle bc-name">{{ fullName(contact) }}</h2>
                    <hr />
                    <p class="bc-title" v-if="contact.job_title">
                        {{ contact.job_title
                        }}<span v-if="contact.company"
                            >, {{ contact.company }}</span
                        >
                    </p>
                </div>
                <div class="bc-contact-details">
                    <ContactsOneToManyList
                        api-name="phone_no"
                        :contact-id="contact.id"
                        :version="contactVersion"
                        v-slot="{ item }"
                    >
                        <div class="bc-item bc-phone-item">
                            <o-icon icon="phone"></o-icon>{{ item.number }}
                        </div>
                    </ContactsOneToManyList>
                    <ContactsOneToManyList
                        ref="emails"
                        @loaded="onEmailsLoaded"
                        api-name="email"
                        :contact-id="contact.id"
                        :version="contactVersion"
                        v-slot="{ item }"
                    >
                        <div class="bc-item bc-email-item">
                            <o-icon icon="envelope"></o-icon
                            ><a :href="'mailto:' + item.email_address">{{
                                item.email_address
                            }}</a>
                        </div>
                    </ContactsOneToManyList>
                    <ContactsOneToManyList
                        v-if="socialMediaSites"
                        api-name="social_media_contact"
                        :contact-id="contact.id"
                        :version="contactVersion"
                        v-slot="{ item }"
                    >
                        <div class="bc-item bc-social-item">
                            <SocialMediaItem
                                :social-media-sites="socialMediaSites"
                                :item="item"
                            ></SocialMediaItem>
                        </div>
                    </ContactsOneToManyList>
                    <ContactsOneToManyList
                        api-name="address"
                        :contact-id="contact.id"
                        :version="contactVersion"
                        v-slot="{ item }"
                    >
                        <div class="bc-item bc-address-item">
                            <o-icon icon="map-marker-alt"></o-icon
                            >{{ concatAddress(item) }}
                        </div>
                    </ContactsOneToManyList>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { getFullName, Contact, concatAddress } from "@/api/contacts";
import ContactsOneToManyList from "@/components/ContactsOneToManyList.vue";
import { getSocialMediaSites } from "@/api/social";
import SocialMediaItem from "@/components/SocialMediaItem.vue";
import UserIcon from "@/components/UserIcon.vue";

export default defineComponent({
    name: "BusinessCard",
    components: { UserIcon, SocialMediaItem, ContactsOneToManyList },
    props: {
        contact: { type: Object as PropType<Contact>, required: true },
        theme: { type: String, default: "default" },
        contactVersion: { type: Number, default: 1 },
    },
    data() {
        return {
            fullName: getFullName,
            concatAddress: concatAddress,
            socialMediaSites: new Map(),
            primaryEmail: null,
        };
    },
    async mounted() {
        this.socialMediaSites = await getSocialMediaSites();
    },
    methods: {
        onEmailsLoaded() {
            const emails = this.$refs.emails as ContactsOneToManyList;
            if (emails.items.length > 0) {
                this.primaryEmail = emails.items[0].email_address;
            }
        },
    },
});
</script>

<style scoped lang="scss">
@import "../styles/variables";
.bc-wrapper {
    width: 30rem;
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
    text-align: center;
    margin-bottom: 1rem;
}

.gravatar-image {
    border-radius: 50%;
    width: 6rem;
    border: 2px solid $grey-dark;
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
    margin-top: 5px;
    margin-bottom: 5px;
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
