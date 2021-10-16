<template>
    <div>
        <div class="hero is-primary is-medium">
            <div class="hero-body">
                <div class="section p-0">
                    <h1 v-if="username" class="title fade-in-text">
                        Hello, {{ username }}.
                    </h1>
                    <h1 v-else>
                        Welcome
                        <div class="progress"></div>
                    </h1>
                </div>
                <div
                    class="
                        section
                        is-flex is-flex-direction-row
                        mt-2
                        p-0
                        fade-in-text
                    "
                >
                    <h1 class="subtitle">
                        Here's what's coming up in the next
                    </h1>
                    <o-select
                        class="ml-3 grey"
                        placeholder="Select timeframe"
                        placeholder-class="primary"
                    >
                        <option value="Day">Day</option>
                        <option value="Week">Week</option>
                        <option value="Fortnight">Fortnight</option>
                        <option value="Month">Month</option>
                    </o-select>
                </div>
            </div>
        </div>
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

<style scoped>
.fade-in-text {
    animation: fadeIn 2s;
}

@keyframes fadeIn {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}
</style>
