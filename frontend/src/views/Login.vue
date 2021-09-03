<template>
    <div>
        <div class="box login-box">
            <img src="../assets/mobius-logo-example.png" class="app-logo" />

            <o-field label="Username">
                <o-input
                    v-model="username"
                    placeholder="Enter 'test'"
                ></o-input>
            </o-field>

            <o-field label="Password">
                <o-input
                    v-model="password"
                    placeholder="Enter 'test'"
                    type="password"
                ></o-input>
            </o-field>

            <div class="login-submit-row">
                <o-button variant="primary" @click="onSubmit">Login</o-button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "Login",
    data() {
        return {
            username: "",
            password: "",
        };
    },
    methods: {
        onSubmit() {
            if (this.username === "test" && this.password === "test") {
                this.$router.push("/app");
            }
        },
    },
});
</script>

<style scoped>
.login-box {
    margin: 10rem auto;
    max-width: 30rem;
}

.login-submit-row {
    text-align: right;
}

.app-logo {
    display: block;
    max-width: 80%;
    margin: 2rem auto;
}
</style>
