// Register the router hooks with their names
import { Vue } from "vue-class-component";

Vue.registerHooks([
    "beforeRouteEnter",
    "beforeRouteLeave",
    "beforeRouteUpdate",
]);
