import Oruga from "@oruga-ui/oruga-next";

import { mount as defaultMount } from "@vue/test-utils";

// most of our components explicitly require Oruga components to be defined,
// so let's make a custom `mount` function which handles that.
export function mount(component, options) {
    if (!options) {
        options = {};
    }
    if (!options.global) {
        options.global = {};
    }
    if (!options.global.plugins) {
        options.global.plugins = [];
    }
    options.global.plugins.push(Oruga);
    return defaultMount(component, options);
}

// window.watchMedia is not implemented by JSDOM,
// so we mock it here to avoid errors
//
// see: https://stackoverflow.com/questions/39830580/jest-test-fails-typeerror-window-matchmedia-is-not-a-function
Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: jest.fn().mockImplementation((query) => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(), // deprecated
        removeListener: jest.fn(), // deprecated
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
    })),
});
