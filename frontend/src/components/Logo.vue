<template>
    <!-- TODO: replace this with final logo once done -->
    <!--<h1
        class="
            page-title
            has-text-primary
            title
            has-text-weight-bold has-text-centered
        "
    >
        möbius
    </h1>-->
    <img :class="'logo ' + type" src="../assets/full_lockup_nobg.png" />
</template>

<script>
export default {
    name: "Logo",
    props: {
        type: {
            Type: String,
            required: false,
        },
    },
};
</script>

<style scoped>
.page-title {
    font-size: 60px;
}
</style>
