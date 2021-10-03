<template>
    <div class="home">
        <nav class="navbar" role="navigation" aria-label="main navigation">
            <div class="navbar-brand">
                <router-link class="navbar-item" to="/">
                    <Logo type="is-small" />
                </router-link>

                <a
                    role="button"
                    class="navbar-burger"
                    aria-label="menu"
                    aria-expanded="false"
                    data-target="navbarBasicExample"
                >
                    <span aria-hidden="true" />
                    <span aria-hidden="true" />
                    <span aria-hidden="true" />
                </a>
            </div>

            <div id="navbarBasicExample" class="navbar-menu">
                <div class="navbar-start">
                    <!--                  <a class="navbar-item">-->
                    <!--                    Home-->
                    <!--                  </a>-->

                    <!--                  <a class="navbar-item">-->
                    <!--                    Documentation-->
                    <!--                  </a>-->

                    <!--                  <div class="navbar-item has-dropdown is-hoverable">-->
                    <!--                    <a class="navbar-link">-->
                    <!--                      More-->
                    <!--                    </a>-->

                    <!--                    <div class="navbar-dropdown">-->
                    <!--                      <a class="navbar-item">-->
                    <!--                        About-->
                    <!--                      </a>-->
                    <!--                      <a class="navbar-item">-->
                    <!--                        Jobs-->
                    <!--                      </a>-->
                    <!--                      <a class="navbar-item">-->
                    <!--                        Contact-->
                    <!--                      </a>-->
                    <!--                      <hr class="navbar-divider">-->
                    <!--                      <a class="navbar-item">-->
                    <!--                        Report an issue-->
                    <!--                      </a>-->
                    <!--                    </div>-->
                    <!--                  </div>-->
                </div>

                <div class="navbar-end">
                    <div class="navbar-item">
                        <div class="buttons">
                            <router-link class="button is-primary" to="/signup">
                                <strong>Sign up</strong>
                            </router-link>
                            <router-link class="button is-warning" to="/login">
                                <strong>Log in</strong>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
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
                        tag="router-link"
                        to="/signup"
                        variant="white is-large"
                        outlined
                        >Get Connected
                    </o-button>
                    <!--                    </router-link>-->
                </div>
                <div class="box has-shadow demo">
                    <video
                        autoplay
                        loop
                        playsinline
                        preload="auto"
                        muted
                        width="800"
                    >
                        <source
                            src="@/assets/demo_mobius.mp4"
                            type="video/mp4"
                        />
                    </video>
                </div>
            </div>
        </section>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Logo from "@/components/Logo.vue";
export default defineComponent({
    name: "Home",
    components: { Logo },
});
</script>

<style scoped>
.desc {
    width: 40%;
    margin: 3rem auto;
}
.demo {
    margin: 0 7rem;
    box-shadow: 0 0.5em 1em -0.125em, 0 0 0 1px;
}
</style>
