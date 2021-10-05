<template>
    <router-view v-slot="{ Component }">
        <!--        <transition name="fade">-->
        <component :is="Component" />
        <!--        </transition>-->
    </router-view>
</template>

<script lang="ts">
import { Vue } from "vue-class-component";

export default class App extends Vue {}
</script>

<style lang="scss">
#app {
    height: 100vh;
}
</style>
