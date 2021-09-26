<template>
    <div class="home">
        <nav class="navbar" role="navigation" aria-label="main navigation">
            <div class="navbar-brand">
                <router-link class="navbar-item" to="/">
                    <img src="../assets/mobius-logo-example.png" />
                </router-link>

                <a
                    role="button"
                    class="navbar-burger"
                    aria-label="menu"
                    aria-expanded="false"
                    data-target="navbarBasicExample"
                >
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
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
                            <router-link class="button is-light" to="/login">
                                Log in
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
        <section class="hero is-large">
            <div class="hero-body">
                <h1 class="title">Möbius CRM</h1>
                <h2 class="subtitle">... connecting you</h2>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: "Home",
};
</script>
