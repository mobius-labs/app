import { mount } from "@vue/test-utils";
import VerificationInput from "../../src/components/VerificationInput.vue";

describe("VerificationInput component unit tests", () => {
    const wrapper = mount(VerificationInput);
    it("is a Vue instance", () => {
        expect(wrapper.findComponent(VerificationInput)).toBeTruthy();
    });
});
