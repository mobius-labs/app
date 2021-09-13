<template>
    <div class="page">
        <div class="box login-box">
            <img src="../assets/mobius-logo-example.png" class="app-logo" />

            <o-field label="Email">
                <o-input
                    v-model="email"
                    placeholder="Enter your email"
                    icon="envelope"
                ></o-input>
            </o-field>

            <o-field label="Password">
                <o-input
                    v-model="password"
                    placeholder="Enter your password"
                    type="password"
                    icon="lock"
                ></o-input>
            </o-field>

            <o-field label="Confirm Password">
                <o-input
                    v-model="confirmedPassword"
                    placeholder="Re-enter password"
                    type="password"
                    icon="arrow-up"
                ></o-input>
            </o-field>
            <div class="">
                <o-button
                    class="is-fullwidth is-medium"
                    variant="primary"
                    @click="onSubmit"
                    >Sign up</o-button
                >
            </div>
        </div>
        <div>
            <p class="alternative">
                Already have an account?
                <a class="link" href="/login">Log in</a>
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "SignUp",
    data() {
        return {
            email: "",
            password: "",
            confirmedPassword: "",
        };
    },
    methods: {
        onSubmit() {
            // would send
            let request = {
                email: this.email,
                password: this.password,
                confirmed: this.confirmedPassword,
            };
            console.log("Would send ", request);

            if (this.password === this.confirmedPassword) {
                // all good! passwords are consistent.
                this.$router.push("/app");
            }
        },
    },
});
</script>

<style scoped>
.login-box {
    max-width: 30rem;
    margin: 3rem auto;
}

.app-logo {
    display: block;
    max-width: 80%;
    margin: 2rem auto;
}

.page {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.3)),
        url("../assets/Presentation1.png");
    justify-content: center;
}

.alternative {
    text-align: center;
    color: white;
}

.link {
    color: yellow;
}
</style>
