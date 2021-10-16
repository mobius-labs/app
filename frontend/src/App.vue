<template>
    <router-view v-slot="{ Component }">
        <transition
            :name="transitionName"
            :mode="transitionMode"
            :enter-active-class="transitionEnterActiveClass"
        >
            <component :is="Component" />
        </transition>
    </router-view>
</template>

<script lang="ts">
import { defineComponent } from "@vue/runtime-core";

const DEFAULT_TRANSITION = "fade";
const DEFAULT_TRANSITION_MODE = "in-out";

export default defineComponent({
    name: "App",
    data() {
        return {
            transitionName: DEFAULT_TRANSITION,
            transitionMode: DEFAULT_TRANSITION_MODE,
            transitionEnterActiveClass: "",
        };
    },
    created() {
        this.$router.beforeEach((to, from, next) => {
            const transitionName = (to.meta.transitionName ||
                from.meta.transitionName ||
                DEFAULT_TRANSITION) as string;

            this.transitionMode = DEFAULT_TRANSITION_MODE;
            this.transitionEnterActiveClass =
                this.transitionName + "-enter-active";

            if (to.meta.transitionName === "zoom") {
                this.transitionMode = "in-out";
                this.transitionEnterActiveClass = "zoom-enter-active";
            }

            if (from.meta.transitionName === "zoom") {
                this.transitionMode = DEFAULT_TRANSITION_MODE;
                this.transitionEnterActiveClass = "";
            }

            this.transitionName = transitionName;

            next();
        });
    },
});
</script>

<style lang="scss">
#app {
    height: 100vh;
    position: relative;
}

.zoom-enter-active,
.zoom-leave-active {
    animation-duration: 0.2s;
    animation-fill-mode: both;
    animation-name: zoom;
}

.zoom-leave-active {
    animation-direction: reverse;
}

@keyframes zoom {
    from {
        opacity: 0;
        transform: scale3d(0.3, 0.3, 0.3);
    }

    100% {
        opacity: 1;
    }
}
</style>
