import { mount } from "./global";
import SocialMediaItem from "../../src/components/SocialMediaItem";

describe("SocialMediaItem component unit tests", () => {
    const MOCK_EMAILS = [
        {
            id: 39,
            email_address: "Foo@Bar.com",
            label: "family",
        },
    ];

    // an example mock contact object to use
    const MOCK_CONTACT = {
        id: 33,
        first_name: "Shivanah",
        social_media: [],
        emails: MOCK_EMAILS,
        addresses: [],
        important_dates: [],
        phone_nos: [],
    };

    const MOCK_SOCIALS = [
        {
            site: "facebook",
            author: MOCK_CONTACT,
        },
    ];
    test("is a Vue instance", () => {
        const wrapper = mount(SocialMediaItem, {
            propsData: {
                socialMediaSites: new Map([["Facebook", MOCK_SOCIALS[0]]]),
                item: {
                    social_media_site: "Facebook",
                    link: "shivshetty",
                },
            },
        });
        expect(wrapper.findComponent(SocialMediaItem)).toBeTruthy();
    });

    test("returns null computed link if item's site is not in list of sites", () => {
        const wrapper = mount(SocialMediaItem, {
            propsData: {
                socialMediaSites: new Map([["Facebook", MOCK_SOCIALS[0]]]),
                item: {
                    social_media_site: "Instagram",
                    link: "shivshetty",
                },
            },
        });
        expect(wrapper.vm.computedLink).toBe(null);
    });
});
