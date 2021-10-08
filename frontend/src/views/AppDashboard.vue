<template>
    <div class="hero is-primary is-medium">
        <div class="hero-body">
            <h1 class="title">Möbius CRM</h1>
        </div>
    </div>
    <div class="content m-4">
        <p>Welcome to Möbius! To get started, use the menu on the left.</p>
    </div>
</template>

<script>
export default {
    name: "AppDashboard",
    mounted() {
        this.$router.replace("/app/contacts");
    },
};
</script>

<style scoped></style>
