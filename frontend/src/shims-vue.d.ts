/* eslint-disable */
declare module "*.vue" {
    import type { DefineComponent } from "vue";
    const component: DefineComponent<{}, {}, any>;
    export default component;

    // import { Component } from "vue";
    // const _default: Component;
    // export default _default;
}
