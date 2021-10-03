// vuex.d.ts
// eslint-disable-next-line no-unused-vars
import { ComponentCustomProperties } from "vue";
import { Store } from "vuex";
import { State } from "@/store";

declare module "@vue/runtime-core" {
    // provide typings for `this.$store`
    // eslint-disable-next-line no-unused-vars
    interface ComponentCustomProperties {
        $store: Store<State>;
    }
}
