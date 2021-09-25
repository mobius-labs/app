<template>
    <div>
        <div class="box login-box">
            <Logo />

            <o-field label="Email">
                <o-input
                    v-model="email"
                    placeholder="Enter your email"
                    required
                    icon="envelope"
                ></o-input>
            </o-field>

            <o-field label="Password">
                <o-input
                    v-model="password"
                    placeholder="Enter your password"
                    required
                    type="password"
                    icon="lock"
                ></o-input>
            </o-field>

            <o-field label="Confirm Password">
                <o-input
                    v-model="confirmedPassword"
                    placeholder="Re-enter password"
                    required
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
                <router-link to="/login" class="has-text-warning"
                    >Log in</router-link
                >
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import Logo from "@/components/Logo.vue";
import { defineComponent } from "vue";
import { displayErrors, getInstance } from "@/api/api";

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
        async onSubmit() {
            // would send
            let data = {
                email: this.email,
                password: this.password,
                confirm_password: this.confirmedPassword,
            };

            let axios = getInstance();

            try {
                let response = await axios.post("account/register", data);
                if (response.data.response === "registration_successful") {
                    this.$oruga.notification.open({
                        message: "Successfully registered user",
                        variant: "success",
                        duration: 10000,
                        closable: true,
                    });
                    await this.$router.push("/");
                }
            } catch (e) {
                if (e.response.data.errors) {
                    displayErrors(e.response, this.$oruga);
                }
                console.log(e.response.data.errors);
            }
        },
    },
});
</script>

<style scoped>
.login-box {
    width: 30rem;
}
</style>
