import Navbar from "../../src/components/Navbar.vue";
import { mount } from "./global";
import MockAdapter from "axios-mock-adapter";
import { getAxiosInstance } from "@/api/api";
import { flushPromises } from "@vue/test-utils";
import { createStore } from "vuex";
import Logo from "../../src/components/Logo";

describe("Navbar component unit tests", () => {
    let mockAxios;
    let store;

    beforeAll(() => {
        // all calls to our `axios` instance should be mocked, since we are testing
        // without a functioning backend server
        // see https://next.vue-test-utils.vuejs.org/guide/advanced/http-requests.html
        mockAxios = new MockAdapter(getAxiosInstance(), {
            onNoMatch: "throwException",
        });

        store = createStore({
            actions: {
                determineAuthStatus() {
                    return true;
                },
            },
        });
    });

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

        const wrapper = mount(Navbar, {
            global: {
                mocks: { $store },
                stubs: ["router-link"],
            },
        });

        expect($store.dispatch).toHaveBeenCalledTimes(1);
        expect($store.dispatch).toHaveBeenCalledWith("determineAuthStatus");
    });

    // test.only("Clicking on Logo routes back to same page", async () => {
    //     const $router = {
    //         push: jest.fn()
    //     }
    //
    //     const wrapper = mount(Navbar, {
    //         global: {
    //             mocks: { $router},
    //             plugins: [store],
    //             stubs: {'router-link': true, 'Logo':Logo}
    //         }
    //     })
    //     console.log(wrapper.html());
    //     console.log('authenticated: '+wrapper.authenticated);
    //
    //     await flushPromises();try{
    //         await wrapper.find("Logo[type='is-small']").trigger('click')
    //     } catch (error) {
    //         console.log(error);
    //     }
    //
    //     expect($router.push).toHaveBeenCalledTimes(1)
    //     expect($router.push).toHaveBeenCalledWith('/')
    // })
});
