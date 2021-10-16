<template>
    <div class="app-layout">
        <nav
            :class="{
                menu: true,
                'app-menu': true,
                'app-menu-dark': darkMode,
                'has-background-grey-darker': darkMode,
            }"
        >
            <div class="level">
                <div class="level-left">
                    <router-link to="/app">
                        <Logo type="is-medium-logo" />
                    </router-link>
                </div>
                <div class="level-right">
                    <o-dropdown aria-role="list">
                        <template #trigger>
                            <UserIcon
                                :email="user ? user.email : null"
                                class="user-profile-container"
                            >
                                <template #fallback>
                                    <div
                                        key="fallback"
                                        style="
                                            position: absolute;
                                            width: 100%;
                                            height: 100%;
                                        "
                                        class="
                                            is-flex
                                            is-align-items-center
                                            is-justify-content-center
                                            user-profile-fallback
                                        "
                                    >
                                        <o-icon
                                            icon="user"
                                            size="medium"
                                            class="user-profile-icon"
                                        />
                                    </div>
                                </template>
                            </UserIcon>
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
                    <!--                    <li>-->
                    <!--                        <router-link to="/app"-->
                    <!--                            ><s>Calendar</s> (coming soon)-->
                    <!--                        </router-link>-->
                    <!--                    </li>-->
                </ul>
                <p class="menu-label">Networking</p>
                <ul class="menu-list">
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
                </ul>
            </div>
        </nav>
        <div class="app-content is-relative">
            <router-view v-slot="{ Component }">
                <transition name="fade">
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
import { User, fetchUserDetails } from "@/api/user";
import UserIcon from "@/components/UserIcon.vue";

@Options({
    components: { UserIcon, Logo },
    watch: { $route: "onRouteUpdated" },
})
export default class AppLayout extends Vue {
    darkMode = false;
    user: User | null = null;

    async mounted() {
        this.onRouteUpdated(this.$route);
        this.user = await fetchUserDetails();
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
    transition: background-color 0.2s ease;
    background-color: $white;
    padding: 16px 16px;
    border-radius: 4px;

    .app-menu-dark & {
        background-color: $grey-dark;

        .menu-label {
            transition: color 0.2s ease;
            color: $grey-lighter;
        }

        .menu-list a {
            transition: color 0.2s ease;
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
    transition: background-color 0.2s ease;
    min-width: 20rem;
    background-color: $info;
    padding: 2rem;
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

.user-profile-container {
    cursor: pointer;
    border-radius: 50%;
    width: 3rem;
    height: 3rem;
    overflow: hidden;
    transition: background-color 0.2s ease, border-color 0.2s ease;

    :deep(img),
    .user-profile-fallback {
        border-radius: 50%;
        border: 2px solid $primary;
    }

    .user-profile-icon {
        color: $primary;
        transition: color 0.2s ease;
    }

    &:hover {
        background-color: lighten($info, 10%);
        border-color: lighten($primary, 10%);

        & .user-profile-icon {
            color: lighten($primary, 10%);
        }
    }
}
</style>
