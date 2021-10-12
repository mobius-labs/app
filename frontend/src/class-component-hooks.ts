// Register the router hooks with their names
// see: https://class-component.vuejs.org/guide/additional-hooks.html

import { Vue } from "vue-class-component";

Vue.registerHooks([
    "beforeRouteEnter",
    "beforeRouteLeave",
    "beforeRouteUpdate",
]);
