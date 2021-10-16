<template>
    <div
        class="is-flex"
        style="height: 100%; position: absolute; left: 0; top: 0; width: 100%"
    >
        <div class="is-flex-1 is-flex is-flex-direction-column">
            <div
                class="has-background-black-ter is-flex"
                style="padding: 2rem; margin-bottom: 0"
            >
                <div>
                    <h1 class="title has-text-white-bis">Business Card</h1>
                    <h2 class="subtitle has-text-grey-light">
                        Share business cards online with colleagues in your
                        network.
                    </h2>
                </div>
                <div class="is-flex-grow-1"></div>
                <o-button
                    variant="dark"
                    icon-left="share-square"
                    class="is-medium"
                    v-if="user && user.business_card"
                    @click="copySharableLink"
                    >Copy link</o-button
                >
            </div>
            <div
                class="
                    is-flex-grow-1
                    is-flex
                    is-flex-direction-column
                    is-align-items-center
                    is-justify-content-center
                    has-background-grey-dark
                "
                style="overflow-y: auto; padding: 5rem 0"
            >
                <BusinessCard
                    preview
                    :contact="updatingTheme ? null : userContact"
                    :theme="updatingTheme ? 'default' : derivedTheme"
                />

                <transition name="fade">
                    <div v-if="user && userContact" class="has-text-centered">
                        <transition-group name="fade">
                            <div
                                class="edit-button"
                                key="edit"
                                v-if="!isEditingContactDetails"
                            >
                                <a @click="shouldEditContactDetails = true"
                                    ><o-icon icon="pencil-alt"></o-icon> Edit
                                    business card content</a
                                >

                                <a
                                    @click="isThemeSelectorModalActive = true"
                                    class="ml-6"
                                    ><o-icon icon="paint-brush"></o-icon> Change
                                    theme</a
                                >
                            </div>

                            <o-switch
                                key="enable"
                                v-if="!isEditingContactDetails"
                                size="large"
                                v-model="user.business_card"
                                class="mt-6"
                            >
                                <span class="has-text-grey-lighter">
                                    <span v-if="user.business_card"
                                        >Business card shared</span
                                    >
                                    <span v-else>Business card private</span>
                                </span>
                            </o-switch>
                        </transition-group>
                    </div>
                </transition>
            </div>
        </div>
        <div
            :class="{ 'right-flyout': true, expanded: isEditingContactDetails }"
        >
            <ContactsEdit
                v-if="isEditingContactDetails"
                ref="contactsEdit"
                :local-id="1"
                :server-id="userContact.id"
                :is-business-card="true"
                @close="tryClose"
                @contact-updated="onContactUpdated"
            >
                <div class="content">
                    <p>
                        If you select to share your business card, then anyone
                        with the link will be able to view the contact details
                        you've entered.
                    </p>

                    <o-switch v-model="user.business_card">
                        <span v-if="user.business_card"
                            >Business card shared</span
                        >
                        <span v-else>Business card private</span>
                    </o-switch>

                    <br /><br />

                    <p>You can also choose from a number of themes</p>

                    <p>
                        <o-button
                            @click="isThemeSelectorModalActive = true"
                            icon-left="paint-brush"
                            variant="dark"
                            >Change theme</o-button
                        >
                    </p>
                </div>

                <hr />
            </ContactsEdit>
        </div>

        <o-modal
            :active="isThemeSelectorModalActive"
            width="1000"
            :on-close="
                (v) => {
                    isThemeSelectorModalActive = false;
                }
            "
            :on-cancel="
                (v) => {
                    isThemeSelectorModalActive = false;
                }
            "
        >
            <div class="modal-card">
                <div class="modal-card-head">
                    <div class="modal-card-title">
                        Choose a theme for your business card
                    </div>
                </div>
                <div class="modal-card-body">
                    <h2 class="subtitle">Built-in Themes</h2>
                    <div class="theme-list">
                        <div
                            class="theme"
                            v-for="(theme, name) in CARD_THEMES"
                            :key="name"
                            @click="selectTheme(name)"
                        >
                            <BusinessCard
                                :contact="userContact"
                                :theme="name"
                                class="theme-card"
                            ></BusinessCard>
                            <p class="theme-label">
                                {{ theme.label }}
                                <strong v-if="derivedTheme === name"
                                    >(current)</strong
                                >
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </o-modal>
    </div>
</template>

<script lang="ts">
import BusinessCard from "@/components/BusinessCard.vue";
import { Contact } from "@/api/contacts";
import ContactsEdit from "@/components/ContactsEdit.vue";
import { defineComponent } from "vue";
import { getAxiosInstance } from "@/api/api";
import { fetchUserDetails, User } from "@/api/user";
import { CARD_THEMES, getTheme } from "@/businessCard";
import { defaultToast } from "@/toasts";
import copy from "copy-to-clipboard";

export default defineComponent({
    name: "BusinessCardEdit",
    components: { BusinessCard, ContactsEdit },
    data() {
        return {
            shouldEditContactDetails: false,
            userContact: null as Contact | null,
            isThemeSelectorModalActive: false,
            user: null as User | null,
            CARD_THEMES: CARD_THEMES,
            fetching: false,
            updatingTheme: false,
        };
    },
    computed: {
        derivedTheme() {
            return getTheme((this as any).user);
        },
        isEditingContactDetails() {
            return (
                (this as any).shouldEditContactDetails &&
                (this as any).userContact
            );
        },
    },
    watch: {
        "user.business_card": "putUserDetails",
        "user.business_card_theme": "updateTheme",
    },
    mounted() {
        this.fetchUserDetails();
        this.fetchUserContact();
    },
    beforeRouteUpdate(to: any, from: any, next: () => void) {
        if (this.$refs.contactsEdit) {
            (
                this.$refs.contactsEdit as typeof ContactsEdit
            ).checkForUnsavedChanges(next);
        } else {
            next();
        }
    },
    beforeRouteLeave(to: any, from: any, next: () => void) {
        if (this.$refs.contactsEdit) {
            (
                this.$refs.contactsEdit as typeof ContactsEdit
            ).checkForUnsavedChanges(next);
        } else {
            next();
        }
    },
    methods: {
        async fetchUserDetails() {
            this.fetching = true;
            this.user = await fetchUserDetails();
            await this.$nextTick(() => {
                this.fetching = false;
            });
        },
        async fetchUserContact() {
            try {
                const result = await getAxiosInstance().get(
                    "/contact_book/get_user_contacts"
                );
                this.userContact = result.data as Contact;
            } catch (e) {
                this.userContact = null;
            }
        },
        async updateTheme() {
            if (this.fetching) {
                return;
            }
            this.updatingTheme = true;
            await this.putUserDetails();
        },
        async putUserDetails() {
            if (this.fetching) {
                return;
            }
            try {
                await getAxiosInstance().put(
                    "/account/update_business_card_visibility",
                    this.user
                );
                this.$oruga.notification.open(
                    defaultToast("info", "Saved preferences")
                );
            } catch (e) {
                console.error(e);
            }
            // this just makes the UI feel cooler
            setTimeout(() => {
                this.updatingTheme = false;
            }, 1000);
        },
        async onContactUpdated() {
            await this.fetchUserContact();
        },

        selectTheme(theme: string) {
            if (this.user) {
                this.user.business_card_theme = theme;
                this.isThemeSelectorModalActive = false;
            }
        },

        copySharableLink() {
            const url =
                location.protocol +
                "//" +
                location.host +
                "/card/" +
                this.user?.email;
            copy(url, { format: "text/plain" });
            this.$oruga.notification.open(
                defaultToast(
                    "info",
                    'Copied link to clipboard: <br /><a href="' +
                        url +
                        '" target="_blank">' +
                        url +
                        "</a>"
                )
            );
        },

        tryClose() {
            if (this.$refs.contactsEdit) {
                (
                    this.$refs.contactsEdit as typeof ContactsEdit
                ).checkForUnsavedChanges(() => {
                    this.shouldEditContactDetails = false;
                });
            }
        },
    },
});
</script>

<style scoped lang="scss">
@import "../styles/flyout.css";
@import "../styles/variables";

.is-flex-1 {
    flex: 1;
}

.edit-button {
    margin-top: 1.5rem;

    a:hover {
        color: lighten($link, 10%);
    }
}

.theme-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
}

.modal-card {
    width: 100%;
}

.theme {
    cursor: pointer;
    border-radius: 0.5rem;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    transition: background-color 0.2s ease;

    &:hover {
        background-color: rgba(0, 0, 0, 0.05);
    }

    .theme-card {
        margin: -1rem;
        pointer-events: none;
        transform: scale(0.8);
    }
}

.theme-label {
    text-align: center;
    font-style: italic;
}
</style>
