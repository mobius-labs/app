import Navbar from "../../src/components/Navbar.vue";
import { mount } from "./global";
import MockAdapter from "axios-mock-adapter";
import { getAxiosInstance } from "@/api/api";
import { createStore } from "vuex";

describe("Navbar component unit tests", () => {
    test("is a Vue instance", () => {
        const $store = {
            dispatch: jest.fn(),
        };
        const wrapper = mount(Navbar, {
            global: {
                mocks: { $store },
                stubs: ["router-link"],
            },
        });
        expect(wrapper.findComponent(Navbar)).toBeTruthy();
    });

    test("determineAuthStatus called when component mounted", () => {
        const $store = {
            dispatch: jest.fn(),
        };

        mount(Navbar, {
            global: {
                mocks: { $store },
                stubs: ["router-link"],
            },
        });

        expect($store.dispatch).toHaveBeenCalledTimes(1);
        expect($store.dispatch).toHaveBeenCalledWith("determineAuthStatus");
    });
});
