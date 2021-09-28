<template>
    <div class="login-page">
        <div class="homepage-link">
            <router-link to="/" class="has-text-warning"
                >Go back to homepage...</router-link
            >
        </div>

        <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
                <component :is="Component"></component>
            </transition>
        </router-view>
    </div>
</template>

<script>
export default {
    name: "AuthLayout",
};
</script>

<style scoped>
.login-page {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.8)),
        url("https://free4kwallpapers.com/uploads/wallpaper/kurzgesagt-wallpaper-2560x1440-wallpaper.jpg")
            no-repeat center center;
    background-size: cover;
    position: relative;
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
