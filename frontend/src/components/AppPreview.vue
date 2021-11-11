<template>
    <div class="box demo">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: "AppPreview",
};
</script>

<style scoped lang="scss">
.demo {
    max-width: 800px;
    margin: 0 7rem;
    padding: 0;
    border: none;
    //box-shadow: 0 0.5em 1em -0.125em;
}

.demo :deep(img),
.demo :deep(video) {
    border-radius: 6px;
    display: block;
}
</style>
