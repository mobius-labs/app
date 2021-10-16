<template>
    <div class="hero is-primary is-medium">
        <div class="hero-body">
            <div class="section p-0">
                <h1 v-if="firstName" class="title is-1 fade-in-text">
                    Hello, {{ firstName }}.
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
                <h1 class="subtitle">Here's what's coming up in the next</h1>
                <o-select class="ml-3 grey" placeholder="Select timeframe">
                    <option value="Day">Day</option>
                    <option value="Week">Week</option>
                    <option value="Fortnight">Fortnight</option>
                    <option value="Month">Month</option>
                </o-select>
            </div>
        </div>
    </div>
    <div>
        <o-collapse
            class="card"
            animation="slide"
            v-for="(collapse, index) of collapses"
            :key="index"
            :open="isOpen == index"
            @open="isOpen = index"
        >
            <template #trigger="props">
                <div class="card-header has-background-white" role="button">
                    <p class="card-header-title has-text-primary">
                        {{ collapse.title }}
                    </p>
                    <a class="card-header-icon">
                        <o-icon :icon="props.open ? 'caret-up' : 'caret-down'">
                        </o-icon>
                    </a>
                </div>
            </template>
            <div class="card-content">
                <div class="content">
                    {{ collapse.text }}
                </div>
            </div>
        </o-collapse>
    </div>
</template>

<script>
import { defineComponent } from "vue";
import { getAxiosInstance } from "@/api/api";

export default defineComponent({
    name: "AppDashboard",
    data() {
        return {
            firstName: null,
            isOpen: 0,
            collapses: [
                {
                    title: "Overdue Catch-ups",
                    text: "Text 1",
                },
                {
                    title: "Upcoming Catch-ups",
                    text: "Text 2",
                },
                {
                    title: "Important Events",
                    text: "Text 3",
                },
            ],
        };
    },
    mounted() {
        this.fetchUserFirstName();
    },
    methods: {
        async fetchUserFirstName() {
            const response = await getAxiosInstance().get("account/getinfo");
            this.firstName = response.data.email;
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

.card {
    background-color: #fff;
    box-shadow: 0 2px 3px hsla(0, 0%, 4%, 0.1), 0 0 0 1px hsla(0, 0%, 4%, 0.1);
    color: #4a4a4a;
    max-width: 100%;
    position: relative;
}
.card-header {
    background-color: transparent;
    align-items: stretch;
    box-shadow: 0 1px 2px hsla(0, 0%, 4%, 0.1);
    display: flex;
}
.card-header-title {
    align-items: center;
    color: #363636;
    display: flex;
    flex-grow: 1;
    font-weight: 700;
    padding: 0.75rem;
    margin: 0;
}
.card-header-icon {
    align-items: center;
    cursor: pointer;
    display: flex;
    padding: 0.75rem;
    justify-content: center;
}
.card-content {
    padding: 1.5rem;
    background-color: transparent;
}
</style>
