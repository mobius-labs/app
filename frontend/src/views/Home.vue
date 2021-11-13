<template>
    <div class="home">
        <Navbar />
        <section class="hero is-large is-primary is-top-half">
            <div class="hero-body is-flex is-justify-content-center" style="">
                <div class="has-text-centered">
                    <p class="title is-1">möbius crm.</p>
                    <p class="subtitle is-3" style="font-weight: 100">
                        Connecting. You.
                    </p>
                    <p class="subtitle is-5 mt-6">
                        Manage your connections, maintain your relationships,
                        and never miss a date!
                    </p>
                </div>
            </div>
        </section>
        <section class="hero is-bottom-half is-relative">
            <div class="hero-body is-flex is-flex-direction-column">
                <AppPreview class="main-preview">
                    <video autoplay loop playsinline preload="auto" muted>
                        <!-- to get around issues with storing videos inside this code repository,
                             we link to demo videos posted to this separate repo: https://github.com/mobius-labs/demo
                             -->
                        <source
                            src="https://user-images.githubusercontent.com/71884945/141427691-bcdb3458-a4ab-4306-b62a-69db1381e559.mp4"
                            type="video/mp4"
                        />
                    </video>
                </AppPreview>
                <div class="video-spacer"></div>
                <div
                    class="blurb has-text-centered mb-6"
                    style="margin-left: auto; margin-right: auto"
                >
                    <p>
                        <o-button
                            v-if="authenticated === true"
                            tag="router-link"
                            to="/app"
                            variant="primary"
                            class="is-large"
                            >Open möbius
                        </o-button>
                        <o-button
                            v-else
                            tag="router-link"
                            to="/signup"
                            variant="primary"
                            class="is-large"
                            >Join Möbius for free
                        </o-button>
                    </p>
                </div>
                <div class="is-flex-grow-1"></div>
                <div class="content has-text-centered" id="features">
                    <hr />
                    <h1 class="title is-size-2" style="margin: 6rem 0 4rem 0">
                        Key features
                    </h1>
                </div>
            </div>
        </section>
        <section class="hero is-info is-medium">
            <div class="hero-body">
                <div
                    class="
                        is-flex-desktop
                        is-align-items-center
                        is-justify-content-space-evenly
                    "
                >
                    <div class="content is-flex-grow-1 blurb">
                        <h1>Store all your contacts</h1>
                        <p>
                            Möbius keeps track of your personal and professional
                            relationships so you don't have to.
                        </p>
                        <p>Key features:</p>
                        <ul>
                            <li>
                                Filter and sort contacts by key attributes such
                                as name, and regularity of contact.
                            </li>
                            <li>
                                Import contacts details directly from a photo of
                                their business card, using AI.
                                <span class="tag is-warning">New!</span>
                            </li>
                        </ul>
                    </div>
                    <AppPreview style="max-width: 600px">
                        <img src="../assets/features/list_contacts.png" />
                    </AppPreview>
                </div>
            </div>
        </section>
        <section class="hero is-medium">
            <div
                class="
                    hero-body
                    is-flex-desktop
                    is-align-items-center
                    is-justify-content-space-evenly
                "
            >
                <AppPreview style="max-width: 400px">
                    <img src="../assets/features/edit_contact.png" />
                </AppPreview>
                <div class="content is-flex-grow-1 blurb">
                    <h1>Add detail to your heart's content</h1>
                    <p>
                        Each contact has a rich assortment of different fields,
                        so you add as much detail as you'd like.
                    </p>
                    <p>Key features:</p>
                    <ul>
                        <li>
                            Unlimited email addresses, phone numbers, social
                            media links, addresses and important dates per
                            contact.
                        </li>
                        <li>
                            Assign labels to email addresses & phone numbers
                            (friend, business, family, other).
                        </li>
                        <li>
                            Common social media sites are recognized, and the
                            site's icon is displayed next to the link.
                        </li>
                        <li>Add free-form notes to any contact.</li>
                        <li>
                            All contact information is automatically saved as
                            you edit.
                        </li>
                    </ul>
                </div>
            </div>
        </section>
        <section class="hero is-medium is-info">
            <div
                class="
                    hero-body
                    is-flex-desktop
                    is-align-items-center
                    is-justify-content-space-evenly
                "
            >
                <div class="content is-flex-grow-1 blurb">
                    <h1>Get reminders about catch-ups and birthdays</h1>
                    <p>
                        The Möbius dashboard reminds you about what's most
                        important in your life.
                    </p>
                    <p>Key features:</p>
                    <ul>
                        <li>
                            Reminders to catch up with contacts, based on the
                            last time you've caught up, and a desired
                            "regularity of contact"
                        </li>
                        <li>
                            Reminders about upcoming important dates (birthdays,
                            anniversaries)
                        </li>
                        <li>Dismiss reminders which aren't important</li>
                        <li>
                            Select how far in the future you want to look (day,
                            week, fortnight, month)
                        </li>
                    </ul>
                </div>
                <AppPreview style="max-width: 600px">
                    <img src="../assets/features/dashboard.png" />
                </AppPreview>
            </div>
        </section>
        <section class="hero is-medium">
            <div
                class="
                    hero-body
                    is-flex-desktop
                    is-align-items-center
                    is-justify-content-space-evenly
                "
            >
                <AppPreview style="max-width: 600px">
                    <img src="../assets/features/edit_bcard.png" />
                </AppPreview>
                <div class="content is-flex-grow-1 blurb">
                    <h1>Share your business card with colleagues</h1>
                    <p>
                        Möbius allows you to create an electronic business card
                        to share with others online.
                    </p>
                    <p>Key features:</p>
                    <ul>
                        <li>
                            Add name, title as well as phone numbers, addresses,
                            social media contacts or a website
                        </li>
                        <li>
                            Add a profile image to your business card using
                            <a
                                href="https://gravatar.com"
                                target="_blank"
                                class="has-text-link"
                                >Gravatar</a
                            >
                        </li>
                        <li>
                            Select from several included themes to express your
                            own personality
                        </li>
                    </ul>
                </div>
            </div>
        </section>
        <section class="hero is-medium is-info">
            <div
                class="
                    hero-body
                    is-flex-desktop
                    is-align-items-center
                    is-justify-content-space-evenly
                "
            >
                <div class="content is-flex-grow-1 blurb">
                    <h1>View business cards and exchange contact details</h1>
                    <p>
                        Received an e-business card from a connection? With
                        Möbius, you can add their contact details to your
                        contact book with one click.
                    </p>
                    <!--                    <p>Key features:</p>-->
                    <!--                    <ul>-->
                    <!--                        <li>Add name, title as well as phone numbers, addresses, social media contacts or a website</li>-->
                    <!--                        <li>Add a profile image to your business card using <a href="https://gravatar.com" target="_blank" class="has-text-link">Gravatar</a></li>-->
                    <!--                        <li>Select from several included themes to express your own personality</li>-->
                    <!--                    </ul>-->
                </div>
                <AppPreview style="max-width: 600px">
                    <img src="../assets/features/view_bcard.png" />
                </AppPreview>
            </div>
        </section>
        <section class="hero is-large" id="about">
            <div class="hero-body">
                <div class="content">
                    <hr />
                    <h1
                        class="title is-size-2 has-text-centered"
                        style="margin: 4rem 0"
                    >
                        About Möbius Labs
                    </h1>
                    <hr class="mb-6" />
                </div>
                <div
                    class="content blurb"
                    style="margin-left: auto; margin-right: auto"
                >
                    <p>
                        möbius crm was developed during the latter half of 2021
                        for as part of the capstone subject for the Computing
                        and Software Systems major at the University of
                        Melbourne, by a team of 5 students.
                    </p>
                </div>
            </div>
        </section>
        <footer class="footer">
            <div class="content has-text-centered">
                <strong>möbius crm</strong>, built with love by
                <em>Möbius Labs</em>. The source code can be found on
                <a href="https://github.com/mobius-labs/app">GitHub</a> under a
                MIT license.
            </div>
        </footer>
    </div>
</template>

<script lang="ts">
import Logo from "@/components/Logo.vue";
import { Options, Vue } from "vue-class-component";
import Navbar from "@/components/Navbar.vue";
import AppPreview from "@/components/AppPreview.vue";

@Options({
    components: { AppPreview, Navbar, Logo },
})
export default class Home extends Vue {
    authenticated: boolean | null = null;

    async mounted() {
        this.authenticated = await this.$store.dispatch("determineAuthStatus");
    }
}
</script>

<style scoped lang="scss">
@import "../styles/variables";
.home {
    height: 100%;
    overflow-y: auto;
}

.blurb {
    max-width: 600px;
}

.is-top-half,
.is-bottom-half {
    min-height: 50vh;
}

.video-spacer {
    height: 200px;
}

.is-top-half {
    box-shadow: inset 0 -11px 8px -12px $grey-dark;
}

.main-preview {
    position: absolute;
    top: -200px;
    left: 0;
    right: 0;
    margin-left: auto;
    margin-right: auto;
    padding: 0.75rem;
}

@media screen and (max-width: 770px) {
    .is-top-half,
    .is-bottom-half {
        min-height: auto;
    }

    .main-preview {
        position: static;
    }

    .video-spacer {
        display: none;
    }
}
</style>
