import "@vue/test-utils";
import HelloWorld from "../../src/components/HelloWorld.vue";

describe("HelloWorld", () => {
    // Check setup is a function
    it("has setup", () => {
        expect(typeof HelloWorld.setup).toBe("function");
    });
});
