<template>
    <div class="box sorry">
        <h1 class="title is-2 is-spaced has-text-primary">
            We're sorry to hear that!
        </h1>
        <h2 class="subtitle">
            Enter your email below, and we'll send you a verification code.
        </h2>
        <o-field>
            <o-input
                v-model="email"
                placeholder="Enter your email"
                type="Email"
                icon="envelope"
            >
            </o-input>
        </o-field>

        <o-tooltip
            label="Please wait a moment before trying to send again."
            position="right"
            :active="!canSendCode"
        >
            <o-button
                variant="primary"
                :disabled="sending || !canSendCode"
                :loading="sending"
                @click="sendData"
            >
                <SpinnerOverlay :active="sending">
                    <span v-if="!codeSent">Send verification code</span>
                    <span v-else>Resend verification code</span>
                </SpinnerOverlay>
            </o-button>
        </o-tooltip>
        <VerificationInput :expanded="codeSent"></VerificationInput>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import VerificationInput from "@/components/VerificationInput.vue";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";

export default defineComponent({
    name: "ForgotPassword",
    components: { SpinnerOverlay, VerificationInput },
    data() {
        return {
            email: "",
            codeSent: false,
            canSendCode: true,
            sending: false,
        };
    },
    methods: {
        sendData() {
            this.sending = true;
            this.codeSent = true;
            // suppose this takes 3s to send
            setTimeout(() => {
                this.sending = false;
                this.canSendCode = false;
            }, 3000);
            setTimeout(() => (this.canSendCode = true), 30000);
            console.log("Would send " + this.email);
        },
    },
});
</script>

<style scoped>
.sorry {
    max-width: 40rem;
}
</style>
