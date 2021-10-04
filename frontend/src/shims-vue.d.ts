/* eslint-disable */
declare module "*.vue" {
    import type { DefineComponent } from "vue";
    const component: DefineComponent<{}, {}, any>;
    export default component;
}

import Oruga from "@oruga-ui/oruga-next";

declare module "@vue/runtime-core" {
    export interface ComponentCustomProperties {
        $oruga: typeof Oruga;
    }
}
