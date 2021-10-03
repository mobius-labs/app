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
html,
body,
#app {
    height: 100%;
    //font-family: Avenir, Helvetica, Arial, sans-serif;
    //-webkit-font-smoothing: antialiased;
    //-moz-osx-font-smoothing: grayscale;
    //text-align: center;
    //color: #2c3e50;
    //margin-top: 60px;
}
</style>
