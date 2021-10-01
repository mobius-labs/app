<template>
    <div class="app">
        <nav class="menu app-menu">
            <div class="level">
                <div class="level-left">
                    <router-link to="/app">
                        <img
                            src="../assets/mobius-logo-example.png"
                            class="app-menu-logo"
                        />
                    </router-link>
                </div>
                <div class="level-right">
                    <div class="user-info">
                        <o-icon icon="user" size="large" />
                    </div>
                </div>
            </div>

            <p class="menu-label">General</p>
            <ul class="menu-list">
                <li>
                    <router-link to="/app/contacts"> Contacts </router-link>
                    <ul>
                        <li><a>Close Friends</a></li>
                        <li><a>Family</a></li>
                        <li><a>Networking</a></li>
                    </ul>
                </li>
                <li>Calendar</li>
            </ul>
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
export default {
    name: "AppLayout",
};
</script>

<style scoped lang="scss">
.app {
    height: 100%;
    display: flex;
    align-items: stretch;
}

.app-menu {
    min-width: 20rem;
    background-color: #eee;
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
