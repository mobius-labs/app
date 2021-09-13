<template>
    <div class="login-page">
        <div class="box login-box">
            <!--<img src="../assets/mobius-logo-example.png" class="app-logo" /> -->
            <h1 class="page-title">möbius</h1>
            <o-field label="Email">
                <o-input
                    v-model="email"
                    placeholder="Enter 'test'"
                    icon="envelope"
                ></o-input>
            </o-field>

            <o-field label="Password">
                <o-input
                    v-model="password"
                    placeholder="Enter 'test'"
                    icon="lock"
                    type="password"
                ></o-input>
            </o-field>
            <p class="forgot"><a href="/forgot">Forgot password?</a></p>
            <div class="login-submit-row">
                <o-button
                    class="is-fullwidth is-medium is-primary"
                    variant=""
                    @click="onSubmit"
                    >Login</o-button
                >
            </div>
        </div>
        <p class="alternative">
            Don't have an account?
            <a href="/signup" style="color: yellow">Sign Up!</a>
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "Login",
    data() {
        return {
            email: "",
            password: "",
        };
    },
    methods: {
        onSubmit() {
            if (this.email === "test" && this.password === "test") {
                this.$router.push("/app");
            }
        },
    },
});
</script>

<style scoped>
.forgot {
    text-align: right;
    margin: 0 0 1rem 0;
}
.login-box {
    display: flex;
    flex-direction: column;
    width: 30rem;
    margin: 0rem auto 0rem auto;
    justify-content: center;
    align-content: center;
}

.page-title {
    font-size: 60px;
    font-weight: bold;
    text-align: center;
    color: dodgerblue;
    margin: 0 auto;
}

.app-logo {
    display: block;
    max-width: 80%;
    margin: 2rem auto;
}

.login-page {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: center;
    align-content: center;
    background: linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 0)),
        url("https://free4kwallpapers.com/uploads/wallpaper/kurzgesagt-wallpaper-2560x1440-wallpaper.jpg");
}
.alternative {
    color: white;
    text-align: center;
}
</style>
