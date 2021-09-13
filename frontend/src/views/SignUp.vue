<template>
    <div>
        <div class="box login-box">
            <Logo />

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
                    icon="redo"
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
            <p class="has-text-centered has-text-white">
                Already have an account?
                <router-link class="link" to="/login">Log in</router-link>
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Logo from "@/components/Logo.vue";

export default defineComponent({
    name: "SignUp",
    components: { Logo },
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
    width: 30rem;
}

.link {
    color: yellow;
}
</style>
