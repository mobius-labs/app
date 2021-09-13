<template>
    <div class="page">
        <div class="box sorry">
            <h1 class="title is-1" style="font-weight: bold; color: dodgerblue">
                We're sorry to hear that!
            </h1>
            <h2 class="title is-4">
                Enter your email below, and we'll send you a verification code.
            </h2>
            <o-field>
                <o-input
                    placeholder="Enter your email"
                    v-model="email"
                    type="Email"
                    icon="envelope"
                >
                </o-input>
            </o-field>
            <o-button variant="primary" @click="sendData"
                >Send verification code</o-button
            >
            <VerificationInput :expanded="codeSent"></VerificationInput>
        </div>
    </div>
</template>

<script lang="ts">
import VerificationInput from "../components/VerificationInput.vue";
import { defineComponent } from "vue";
export default defineComponent({
    name: "ForgotPassword",
    components: { VerificationInput },
    data() {
        return {
            email: "",
            codeSent: false,
        };
    },
    methods: {
        sendData() {
            this.codeSent = true;
            console.log("Would send " + this.email);
        },
    },
});
</script>

<style scoped>
.page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    background: linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.3)),
        url("https://free4kwallpapers.com/uploads/wallpaper/kurzgesagt-wallpaper-2560x1440-wallpaper.jpg");
}

.sorry {
    max-width: 30rem;
    margin: 20rem auto;
    vertical-align: center;
}
</style>
