import { createApp } from "vue";
import "./class-component-hooks";
import App from "./App.vue";
import Oruga from "@oruga-ui/oruga-next";
import "@oruga-ui/oruga-next/dist/oruga-full.css";
import { bulmaConfig } from "my-vue-app/src/plugins/oruga";
import router from "./router";

import "./styles/app.scss";

import "@fortawesome/fontawesome-free/scss/fontawesome.scss";
import "@fortawesome/fontawesome-free/scss/regular.scss";
import "@fortawesome/fontawesome-free/scss/solid.scss";
import "@fortawesome/fontawesome-free/scss/brands.scss";
import { setStore, setOrugaInstance, setRouterInstance } from "@/api/api";
import store from "./store";

// this makes Typescript no longer complain about a missing
// "this.$oruga" property on Vue components.
declare module "@vue/runtime-core" {
    export interface ComponentCustomProperties {
        $oruga: typeof Oruga;
    }
}

const app = createApp(App);
app.use(store);
app.use(router);
app.use(Oruga, {
    iconPack: "fas",
    ...bulmaConfig,
});

const root = app.mount("#app");
setOrugaInstance(root.$oruga);
setRouterInstance(router);
setStore(store);
