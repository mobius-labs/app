import InlineSelect from "../../src/components/InlineSelect.vue";
import { mount } from "./global";
import MockAdapter from "axios-mock-adapter";
import { getAxiosInstance } from "@/api/api";
import { flushPromises } from "@vue/test-utils";
import ContactsEdit from "../../src/components/ContactsEdit";

describe("InlineSelect component unit tests", () => {
    let mockAxios;

    const SELECT_PROPS = {
        options: { work: "work", personal: "personal", family: "family" },
        modelValue: "work",
    };

    const UNSELECTED = [
        ["personal", "personal"],
        ["family", "family"],
    ];

    beforeAll(() => {
        // all calls to our `axios` instance should be mocked, since we are testing
        // without a functioning backend server
        // see https://next.vue-test-utils.vuejs.org/guide/advanced/http-requests.html
        mockAxios = new MockAdapter(getAxiosInstance(), {
            onNoMatch: "throwException",
        });
    });

    test("is a Vue instance", () => {
        const wrapper = mount(InlineSelect, {
            propsData: SELECT_PROPS,
        });
        expect(wrapper.findComponent(InlineSelect)).toBeTruthy();
    });

    test("creates computed properties", () => {
        const wrapper = mount(InlineSelect, {
            propsData: SELECT_PROPS,
        });
        expect(wrapper.vm.display).toEqual(SELECT_PROPS.modelValue);
        expect(wrapper.vm.notCurrentlySelectedOptions).toEqual(UNSELECTED);
    });

    test("displays selected value", () => {
        const wrapper = mount(InlineSelect, {
            propsData: SELECT_PROPS,
            slots: { trigger: "true" },
        });
        expect(wrapper.find("span.underlined").text()).toContain(
            wrapper.vm.display
        );
    });
});
