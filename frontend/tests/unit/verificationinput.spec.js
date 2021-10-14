import VerificationInput from "../../src/components/VerificationInput.vue";
import { mount } from "./global";

describe("VerificationInput component unit tests", () => {
    const wrapper = mount(VerificationInput);
    it("is a Vue instance", () => {
        expect(wrapper.findComponent(VerificationInput)).toBeTruthy();
    });
});
