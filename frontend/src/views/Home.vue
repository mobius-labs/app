<template>
    <div class="home">
        <Navbar />
        <section
            class="
                hero
                is-primary is-fullheight-with-navbar
                has-content-centered
            "
        >
            <div class="hero-body">
                <div class="container has-text-centered">
                    <p class="title is-1">möbius crm.</p>
                    <p class="subtitle is-4">Connecting. You.</p>
                    <div class="container">
                        <p class="desc subtitle is-6">
                            Manage your connections, maintain your
                            relationships, and never miss a date!
                        </p>
                    </div>
                    <!--<o-button variant="white is-large" outlined
                    >Get Connected
                    </o-button>-->
                    <!--                    <router-link >-->

                    <o-button
                        v-if="authenticated === true"
                        tag="router-link"
                        to="/app"
                        variant="white is-large"
                        outlined
                        >Open möbius
                    </o-button>
                    <o-button
                        v-else
                        tag="router-link"
                        to="/signup"
                        variant="white is-large"
                        outlined
                        >Get Connected
                    </o-button>
                    <!--                    </router-link>-->
                </div>
                <div class="box demo">
                    <video
                        autoplay
                        loop
                        playsinline
                        preload="auto"
                        muted
                        width="800"
                    >
                        <!-- to get around issues with storing videos inside this code repository,
                             we link to demo videos posted to this separate repo: https://github.com/mobius-labs/demo
                             -->
                        <source
                            src="https://user-images.githubusercontent.com/7961339/139358825-514b3358-3658-48d9-ba98-edb1ed325b87.mp4"
                            type="video/mp4"
                        />
                    </video>
                </div>
            </div>
        </section>
    </div>
</template>

<script lang="ts">
import Logo from "@/components/Logo.vue";
import { Options, Vue } from "vue-class-component";
import Navbar from "@/components/Navbar.vue";

@Options({
    components: { Navbar, Logo },
})
export default class Home extends Vue {
    authenticated: boolean | null = null;

    async mounted() {
        this.authenticated = await this.$store.dispatch("determineAuthStatus");
    }
}
</script>

<style scoped lang="scss">
.desc {
    width: 40%;
    margin: 3rem auto;
}
.demo {
    margin: 0 7rem;
    box-shadow: 0 0.5em 1em -0.125em, 0 0 0 1px;
    padding: 1rem;

    video {
        border-radius: 6px;
        display: block;
    }
}
</style>
