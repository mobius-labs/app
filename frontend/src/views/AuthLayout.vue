<template>
    <div class="hero is-fullheight is-primary auth-page">
        <div class="homepage-link">
            <router-link to="/" class="has-text-white"
                >Go back to homepage...</router-link
            >
        </div>

        <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
                <component :is="Component" />
            </transition>
        </router-view>
    </div>
</template>

<script>
export default {
    name: "AuthLayout",
};
</script>

<style scoped lang="scss">
@import "../styles/app.scss";

.auth-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 100;
}

.homepage-link {
    position: absolute;
    top: 1rem;
    left: 0;
    display: flex;
    justify-content: center;
    width: 100%;
}
</style>
