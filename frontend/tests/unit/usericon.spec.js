import UserIcon from "../../src/components/UserIcon";
import { mount } from "./global";

describe("UserIcon component unit tests", () => {
    let wrapper;

    beforeAll(() => {
        wrapper = mount(UserIcon, {
            propsData: {
                email: "test@gmail.com",
            },
            data() {
                return { gravatarLoaded: true };
            },
        });
    });

    test("is a Vue instance", () => {
        expect(wrapper.findComponent(UserIcon)).toBeTruthy();
    });

    test("gravatarIconSrc is null when provided with no email", async () => {
        await wrapper.setProps({ email: null });
        expect(wrapper.vm.gravatarIconSrc).toEqual(null);
    });

    test("onGravatarLoaded called when image is loading", async () => {
        await wrapper.setProps({ email: "test@gmail.com" });
        await wrapper.setData({ gravatarLoaded: false });

        wrapper.find("img.img").trigger("load");
        expect(wrapper.vm.gravatarLoaded).toEqual(true);
    });

    test("onGravatarLoadError called when load error occurs", async () => {
        await wrapper.setData({ gravatarLoaded: true });

        wrapper.find("img.img").trigger("error");
        expect(wrapper.vm.gravatarLoaded).toEqual(false);
    });
});
