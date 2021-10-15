<template>
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
                @click="isActive = !isActive"
            >
                <span aria-hidden="true" />
                <span aria-hidden="true" />
                <span aria-hidden="true" />
            </a>
        </div>

        <div
            id="navbarBasicExample"
            :class="{ 'navbar-menu': true, 'is-active': isActive }"
        >
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
                    <div v-if="authenticated === false" class="buttons">
                        <router-link class="button is-primary" to="/signup">
                            <strong>Sign up</strong>
                        </router-link>
                        <router-link class="button is-warning" to="/login">
                            <strong>Log in</strong>
                        </router-link>
                    </div>
                    <div
                        v-else-if="authenticated === true"
                        class="is-flex is-align-items-center"
                    >
                        You're already logged in
                        <router-link to="/app" class="button is-info ml-3"
                            ><strong>Open möbius</strong></router-link
                        >
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Logo from "@/components/Logo.vue";

export default defineComponent({
    name: "Navbar",
    components: { Logo },
    data() {
        return {
            authenticated: null as boolean | null,
            isActive: false,
        };
    },
    async mounted() {
        this.authenticated = await this.$store.dispatch("determineAuthStatus");
    },
});
</script>

<style scoped></style>
