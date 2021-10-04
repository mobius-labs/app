<template>
    <div class="login-box">
        <div class="box">
            <div class="has-text-centered">
                <Logo type="is-large-logo" />
            </div>

            <NonFieldErrorsList :non-field-errors="serverData.nonFieldErrors" />

            <ValidatedField
                v-slot="{ value, setValue }"
                v-model="model"
                name="username"
                label="Email"
                :server-data="serverData"
            >
                <o-input
                    :model-value="value"
                    placeholder="Enter your email"
                    icon="envelope"
                    required
                    @update:model-value="setValue"
                />
            </ValidatedField>

            <ValidatedField
                v-slot="{ value, setValue }"
                v-model="model"
                label="Password"
                name="password"
                :server-data="serverData"
            >
                <o-input
                    :model-value="value"
                    placeholder="************"
                    icon="lock"
                    type="password"
                    required
                    @update:model-value="setValue"
                    @keyup.enter="onSubmit"
                />
            </ValidatedField>
            <p class="has-text-right mb-4">
                <router-link to="/forgot">Forgot password?</router-link>
            </p>
            <div>
                <o-button
                    class="is-fullwidth is-medium is-primary"
                    variant=""
                    :disabled="submitting"
                    @click="onSubmit"
                >
                    <SpinnerOverlay :active="submitting">
                        Login
                    </SpinnerOverlay>
                </o-button>
            </div>
        </div>
        <p class="has-text-white has-text-centered">
            Don't have an account?
            <router-link to="/signup" class="has-text-warning">
                Sign Up!
            </router-link>
        </p>
    </div>
</template>

<script lang="ts">
import Logo from "@/components/Logo.vue";
import { Options, Vue } from "vue-class-component";
import { getAxiosInstance, ServerData } from "@/api/api";
import ValidatedField from "@/components/ValidatedField.vue";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";
import NonFieldErrorsList from "@/components/NonFieldErrorsList.vue";

@Options({
    components: { NonFieldErrorsList, SpinnerOverlay, ValidatedField, Logo },
})
export default class Login extends Vue {
    model = {
        username: "",
        password: "",
    };
    serverData = new ServerData();
    submitting = false;

    async onSubmit() {
        try {
            this.submitting = true;
            let response = await getAxiosInstance().post(
                "account/login",
                this.model
            );
            await this.$store.dispatch("login", {
                token: response.data.token,
                router: this.$router,
                oruga: this.$oruga,
            });
        } catch (e) {
            this.serverData.handleError(e, this.model);
        }
        this.submitting = false;
    }
}
</script>

<style scoped>
.login-box {
    width: 30rem;
}
</style>
