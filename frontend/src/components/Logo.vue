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
    <img
        :class="'logo ' + type"
        src="../assets/full_lockup_nobg.png"
        alt="Möbius Labs Logo"
    />
</template>

<script>
export default {
    name: "Logo",
    props: {
        type: {
            type: String,
            required: false,
        },
    },
};
</script>

<style scoped lang="scss">
// Set some custom image sizes for the logo on different pages
$large-width-logo: 18rem;
$medium-width-logo: 10rem;
$small-width-logo: 6.5rem;

.is-large-logo {
    width: $large-width-logo;
    height: auto;
}

.is-medium-logo {
    width: $medium-width-logo;
    height: auto;
}

.is-small-logo {
    width: $small-width-logo;
    height: auto;
}

.page-title {
    font-size: 60px;
}
</style>
