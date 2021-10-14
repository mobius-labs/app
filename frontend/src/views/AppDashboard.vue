<template>
    <div class="hero is-primary is-medium">
        <div class="hero-body">
            <h1 v-if="username" class="title">Welcome, {{ username }}.</h1>
            <h1 v-else>
                Welcome
                <div class="progress"></div>
            </h1>
            <h1 class="subtitle">Here's what's coming up:</h1>
        </div>
    </div>
    <div class="content m-4">
        <p>Welcome to Möbius! To get started, use the menu on the left.</p>
    </div>
</template>

<script>
import { defineComponent } from "vue";
import { getAxiosInstance } from "@/api/api";

export default defineComponent({
    name: "AppDashboard",
    data() {
        return {
            username: null,
        };
    },
    mounted() {
        this.fetchUsername();
    },
    methods: {
        async fetchUsername() {
            const response = await getAxiosInstance().get("account/getinfo");
            this.username = response.data;
        },
    },
});
</script>

<style scoped></style>
