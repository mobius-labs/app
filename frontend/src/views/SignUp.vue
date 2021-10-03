<template>
    <div>
        <div class="box login-box">
            <div class="has-text-centered">
                <Logo type="is-large-logo" />
            </div>

            <NonFieldErrorsList :non-field-errors="serverData.nonFieldErrors" />

            <ValidatedField
                v-slot="{ value, setValue }"
                v-model="model"
                name="email"
                label="Email"
                :server-data="serverData"
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
                v-model="model"
                label="Password"
                name="password"
                :server-data="serverData"
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
                v-model="model"
                label="Confirm Password"
                name="confirm_password"
                :server-data="serverData"
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
                    :disabled="submitting"
                    @click="onSubmit"
                >
                    <SpinnerOverlay :active="submitting">
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
import { getAxiosInstance, ServerData } from "@/api/api";
import { Options, Vue } from "vue-class-component";
import ValidatedField from "@/components/ValidatedField.vue";
import NonFieldErrorsList from "@/components/NonFieldErrorsList.vue";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";

@Options({
    components: { ValidatedField, Logo, SpinnerOverlay, NonFieldErrorsList },
})
export default class SignUp extends Vue {
    model = {
        email: "",
        password: "",
        confirm_password: "",
    };
    serverData = new ServerData();
    submitting = false;

    async onSubmit() {
        try {
            this.submitting = true;
            // we want to "deep copy" the object so changing one doesn't change the other.
            let response = await getAxiosInstance().post(
                "account/register",
                this.model
            );
            if (response.data.response === "registration_successful") {
                await this.$store.dispatch("login", {
                    token: response.data.token,
                    router: this.$router,
                    oruga: this.$oruga,
                });
            }
        } catch (e) {
            this.serverData.fromValidationError(e, this.model);
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
