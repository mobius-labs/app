<template>
    <div class="login-box">
        <div class="box">
            <div class="has-text-centered">
                <Logo type="is-large-logo" />
            </div>

            <NonFieldErrorsList :model="model" />

            <ValidatedField
                :model="model"
                name="username"
                label="Email"
                placeholder="Enter your email"
                icon="envelope"
                required
            ></ValidatedField>

            <ValidatedField
                v-slot="{ value, setValue }"
                :model="model"
                label="Password"
                name="password"
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
                    :disabled="model.isSubmitting"
                    @click="onSubmit"
                >
                    <SpinnerOverlay :active="model.isSubmitting">
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
import { getAxiosInstance } from "@/api/api";
import ValidatedField from "@/components/ValidatedField.vue";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";
import NonFieldErrorsList from "@/components/NonFieldErrorsList.vue";
import { defaultToast } from "@/toasts";
import { Model } from "@/api/model";

interface SuccessfulLoginResponse {
    token: string;
}

@Options({
    components: { NonFieldErrorsList, SpinnerOverlay, ValidatedField, Logo },
})
export default class Login extends Vue {
    model = new Model({
        username: "",
        password: "",
    });

    async created() {
        if (await this.$store.dispatch("determineAuthStatus")) {
            this.$oruga.notification.open(
                defaultToast("info", "You're already logged in.")
            );
            await this.$router.replace("/app");
        }
    }

    async onSubmit() {
        await this.model.tryUpdate(async () => {
            const response = await getAxiosInstance().post(
                "account/login",
                this.model.model
            );
            await this.$store.dispatch("login", {
                token: (response.data as SuccessfulLoginResponse).token,
                router: this.$router,
                oruga: this.$oruga,
            });
        });
    }
}
</script>

<style scoped>
.login-box {
    width: 30rem;
}
</style>
