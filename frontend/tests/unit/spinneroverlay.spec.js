import { mount } from "@vue/test-utils";
import SpinnerOverlay from "../../src/components/SpinnerOverlay.vue";

describe("SpinnerOverlay component unit tests", () => {
    it("is a Vue instance", () => {
        const wrapper = mount(SpinnerOverlay);
        expect(wrapper.findComponent(SpinnerOverlay)).toBeTruthy();
    });

    it("displays if active is true", () => {
        const wrapper = mount(SpinnerOverlay, {
            propsData: { active: true },
        });
        expect(wrapper.find("o-icon").exists()).toBeTruthy();
    });
});
