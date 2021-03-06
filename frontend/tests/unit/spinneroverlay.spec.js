import SpinnerOverlay from "../../src/components/SpinnerOverlay.vue";
import { mount } from "./global";
import Spinner from "../../src/components/Spinner";

describe("SpinnerOverlay component unit tests", () => {
    it("is a Vue instance", () => {
        const wrapper = mount(SpinnerOverlay);
        expect(wrapper.findComponent(SpinnerOverlay)).toBeTruthy();
    });

    it("displays if active is true", () => {
        const wrapper = mount(SpinnerOverlay, {
            propsData: { active: true },
        });
        expect(wrapper.findComponent(Spinner).exists()).toBeTruthy();
    });
});
