<template>
    <o-icon icon="spinner" :size="size" class="spin-always" />
</template>

<script>
export default {
    name: "Spinner",
    props: {
        size: { type: String, default: null },
    },
};
</script>

<style scoped>
.spin-always {
    z-index: 10;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>
