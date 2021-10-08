<template>
    <div class="app-layout">
        <nav class="menu app-menu">
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
                    <!--                    <li>-->
                    <!--                        <router-link to="/app"> Dashboard </router-link>-->
                    <!--                    </li>-->
                    <li>
                        <router-link to="/app/contacts">Contacts</router-link>
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
            <!--              <p class="menu-label">-->
            <!--                Administration-->
            <!--              </p>-->
            <!--              <ul class="menu-list">-->
            <!--                <li><a>Team Settings</a></li>-->
            <!--                <li>-->

            <!--                </li>-->
            <!--                <li><a>Invitations</a></li>-->
            <!--                <li><a>Cloud Storage Environment Settings</a></li>-->
            <!--                <li><a>Authentication</a></li>-->
            <!--              </ul>-->
            <!--              <p class="menu-label">-->
            <!--                Transactions-->
            <!--              </p>-->
            <!--              <ul class="menu-list">-->
            <!--                <li><a>Payments</a></li>-->
            <!--                <li><a>Transfers</a></li>-->
            <!--                <li><a>Balance</a></li>-->
            <!--              </ul>-->
        </nav>
        <div class="app-content">
            <router-view />
        </div>
    </div>
</template>

<script>
import Logo from "@/components/Logo.vue";
import { Options, Vue } from "vue-class-component";

@Options({
    components: { Logo },
})
export default class AppLayout extends Vue {
    async logout() {
        await this.$store.dispatch("logout", {
            router: this.$router,
            oruga: this.$oruga,
        });
    }
}
</script>

<style scoped lang="scss">
@import "../styles/variables.scss";

.menu-items {
    background-color: $white;
    padding: 16px 16px;
    border-radius: 4px;
}

.app-layout {
    height: 100vh;
    display: flex;
    align-items: stretch;
}

.app-menu {
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
</style>
