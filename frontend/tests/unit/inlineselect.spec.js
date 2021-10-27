import InlineSelect from "../../src/components/InlineSelect.vue";
import { mount } from "./global";

describe("InlineSelect component unit tests", () => {
    const SELECT_PROPS = {
        options: { work: "work", personal: "personal", family: "family" },
        modelValue: "work",
    };

    const UNSELECTED = [
        ["personal", "personal"],
        ["family", "family"],
    ];

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
