<template>
    <div class="login-box">
        <div class="box">
            <Logo />
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
            <p class="has-text-right mb-4">
                <router-link to="/forgot">Forgot password?</router-link>
            </p>
            <div>
                <o-button
                    class="is-fullwidth is-medium is-primary"
                    variant=""
                    @click="onSubmit"
                    >Login</o-button
                >
            </div>
        </div>
        <p class="has-text-white has-text-centered">
            Don't have an account?
            <router-link to="/signup" class="has-text-warning"
                >Sign Up!</router-link
            >
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Logo from "@/components/Logo.vue";

export default defineComponent({
    name: "Login",
    components: { Logo },
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
.login-box {
    width: 25rem;
}
</style>
