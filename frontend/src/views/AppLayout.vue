<template>
    <div class="app-layout">
        <nav
            :class="{ menu: true, 'app-menu': true, 'app-menu-dark': darkMode }"
        >
            <div class="level">
                <div class="level-left">
                    <!--<router-link to="/app">
                        <img
                            src="../assets/mobius-logo-example.png"
                            class="app-menu-logo"
                        />
                    </router-link>-->
                    <router-link to="/app">
                        <Logo type="is-medium-logo" />
                    </router-link>
                </div>
                <div class="level-right">
                    <o-dropdown aria-role="list">
                        <template #trigger>
                            <o-button variant="info">
                                <!--                                <div class="user-info">-->
                                <o-icon
                                    icon="user"
                                    size="medium"
                                    variant="primary"
                                />
                                <!--                                </div>-->
                                <!--                                <o-icon :icon="active ? 'caret-up' : 'caret-down'"></o-icon>-->
                            </o-button>
                        </template>

                        <!--                        <o-dropdown-item aria-role="listitem">Action</o-dropdown-item>-->
                        <!--                        <o-dropdown-item aria-role="listitem">Another action</o-dropdown-item>-->
                        <o-dropdown-item aria-role="listitem" @click="logout"
                            >Logout</o-dropdown-item
                        >
                    </o-dropdown>
                </div>
            </div>
            <div class="menu-items">
                <p class="menu-label">General</p>
                <ul class="menu-list">
                    <li>
                        <router-link to="/app"> Dashboard </router-link>
                    </li>
                    <li>
                        <router-link to="/app/contacts">Contacts</router-link>
                        <!--                    <ul>-->
                        <!--                        <li><a>Close Friends</a></li>-->
                        <!--                        <li><a>Family</a></li>-->
                        <!--                        <li><a>Networking</a></li>-->
                        <!--                    </ul>-->
                    </li>
                    <li>
                        <router-link to="/app/business-card"
                            >Business Card
                            <span class="tag is-warning ml-1"
                                >New!</span
                            ></router-link
                        >
                        <!--                    <ul>-->
                        <!--                        <li><a>Close Friends</a></li>-->
                        <!--                        <li><a>Family</a></li>-->
                        <!--                        <li><a>Networking</a></li>-->
                        <!--                    </ul>-->
                    </li>
                    <li>
                        <router-link to="/app"
                            ><s>Calendar</s> (coming soon)
                        </router-link>
                    </li>
                </ul>
            </div>
        </nav>
        <div class="app-content">
            <router-view v-slot="{ Component, route }">
                <transition :name="route.meta.transitionName">
                    <component :is="Component"></component>
                </transition>
            </router-view>
        </div>
    </div>
</template>

<script lang="ts">
import Logo from "@/components/Logo.vue";
import { Options, Vue } from "vue-class-component";
import { RouteLocationNormalized } from "vue-router";

@Options({
    components: { Logo },
    watch: { $route: "onRouteUpdated" },
})
export default class AppLayout extends Vue {
    darkMode = false;

    mounted() {
        this.onRouteUpdated(this.$route);
    }

    async logout() {
        await this.$store.dispatch("logout", {
            router: this.$router,
            oruga: this.$oruga,
        });
    }

    onRouteUpdated(route: RouteLocationNormalized) {
        this.darkMode = !!route.meta.darkMode;
    }
}
</script>

<style scoped lang="scss">
@import "../styles/variables.scss";

.menu-items {
    transition: background-color 0.5s ease;
    background-color: $white;
    padding: 16px 16px;
    border-radius: 4px;

    .app-menu-dark & {
        transition: background-color 0.5s ease;
        background-color: $grey;

        .menu-label {
            transition: color 0.5s ease;
            color: $grey-lighter;
        }

        .menu-list a {
            transition: color 0.5s ease;
            color: $grey-lighter;

            &:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        }
    }
}

.app-layout {
    height: 100vh;
    display: flex;
    align-items: stretch;
}

.app-menu {
    transition: background-color 1s ease;
    min-width: 20rem;
    background-color: $info;
    padding: 2rem;
}

.app-menu-dark {
    background-color: $grey-dark;
}

.app-content {
    flex: 1;
}

.app-menu-logo {
    width: 10rem;
}

.home-row {
    display: flex;
    justify-content: space-between;
}
</style>
