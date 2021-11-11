<template>
    <div class="login-box">
        <div class="box">
            <div class="has-text-centered">
                <Logo type="is-large-logo" />
            </div>

            <NonFieldErrorsList :model="model" />

            <ValidatedField
                v-slot="{ value, setValue }"
                :model="model"
                name="email"
                label="Email"
            >
                <o-input
                    :model-value="value"
                    placeholder="Enter your email"
                    required
                    icon="envelope"
                    @update:model-value="setValue"
                />
            </ValidatedField>

            <ValidatedField
                v-slot="{ value, setValue }"
                :model="model"
                label="Password"
                name="password"
            >
                <o-input
                    :model-value="value"
                    placeholder="Enter your password"
                    required
                    type="password"
                    icon="lock"
                    @update:model-value="setValue"
                />
            </ValidatedField>

            <ValidatedField
                v-slot="{ value, setValue }"
                :model="model"
                label="Confirm Password"
                name="confirm_password"
            >
                <o-input
                    :model-value="value"
                    placeholder="Re-enter password"
                    required
                    type="password"
                    icon="redo"
                    @update:model-value="setValue"
                    @keyup.enter="onSubmit"
                />
            </ValidatedField>
            <div>
                <o-button
                    class="is-fullwidth is-medium"
                    variant="primary"
                    :disabled="model.isSubmitting"
                    @click="onSubmit"
                >
                    <SpinnerOverlay :active="model.isSubmitting">
                        Sign up
                    </SpinnerOverlay>
                </o-button>
            </div>
        </div>
        <div>
            <p class="has-text-centered has-text-white">
                Already have an account?
                <router-link to="/login" class="has-text-warning">
                    Log in
                </router-link>
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import Logo from "@/components/Logo.vue";
import { getAxiosInstance } from "@/api/api";
import { Options, Vue } from "vue-class-component";
import ValidatedField from "@/components/ValidatedField.vue";
import NonFieldErrorsList from "@/components/NonFieldErrorsList.vue";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";
import { defaultToast } from "@/toasts";
import { Model } from "@/api/model";

interface SuccessfulRegisterResponse {
    response: string;
    token: string;
}

@Options({
    components: { ValidatedField, Logo, SpinnerOverlay, NonFieldErrorsList },
})
export default class SignUp extends Vue {
    model = new Model({
        email: "",
        password: "",
        confirm_password: "",
    });

    async created() {
        if (await this.$store.dispatch("determineAuthStatus")) {
            this.$oruga.notification.open(
                defaultToast(
                    "info",
                    "Cannot sign up - you're already logged in."
                )
            );
            await this.$router.replace("/app");
        }
    }

    async onSubmit() {
        await this.model.tryUpdate(async () => {
            const response = await getAxiosInstance().post(
                "account/register",
                this.model.model
            );
            const data = response.data as SuccessfulRegisterResponse;
            if (data.response === "registration_successful") {
                await this.$store.dispatch("login", {
                    token: data.token,
                    router: this.$router,
                    oruga: this.$oruga,
                    isSignUp: true,
                });
            }
        });
    }
}
</script>

<style scoped lang="scss">
@import "../styles/login";
</style>
