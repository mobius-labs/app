<template>
    <div>
        <div class="icon-container">
            <o-icon v-if="active" icon="spinner" class="spin-always" />
        </div>
        <div :class="active ? 'hide-text' : ''">
            <slot />
        </div>
    </div>
</template>

<script>
import { Options, Vue } from "vue-class-component";

@Options({
    props: {
        active: {
            type: Boolean,
            default: true,
        },
    },
})
export default class SpinnerOverlay extends Vue {}
</script>

<style scoped>
@keyframes spin {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}

.icon-container {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

.hide-text {
    visibility: hidden;
}

.spin-always {
    z-index: 10;
    animation: spin 1s linear infinite;
}
</style>
