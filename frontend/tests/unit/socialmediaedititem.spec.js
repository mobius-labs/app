import { mount } from "./global";
import MockAdapter from "axios-mock-adapter";
import { getAxiosInstance } from "@/api/api";
import SocialMediaEditItem from "../../src/components/SocialMediaItem";

describe("SocialMediaEditItem component unit tests", () => {
    let mockAxios;
    let wrapper;

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

    beforeAll(() => {
        // all calls to our `axios` instance should be mocked, since we are testing
        // without a functioning backend server
        // see https://next.vue-test-utils.vuejs.org/guide/advanced/http-requests.html
        mockAxios = new MockAdapter(getAxiosInstance(), {
            onNoMatch: "throwException",
        });

        wrapper = mount(SocialMediaEditItem, {
            propsData: {
                socialMediaSites: new Map([["Facebook", MOCK_SOCIALS[0]]]),
                model: {
                    social_media_site: "Facebook",
                    link: "shivshetty",
                },
                item: {
                    social_media_site: "Facebook",
                    link: "shivshetty",
                },
            },
        });
    });

    beforeEach(() => {
        // mocks general info required by this component
        mockAxios
            .onGet("/contact_book/get_social_media_sites/")
            .reply(200, MOCK_SOCIALS);
    });

    test("is a Vue instance", () => {
        expect(wrapper.findComponent(SocialMediaEditItem)).toBeTruthy();
    });

    // test.only("class attributes are correct", () => {
    //     expect(wrapper.vm.shouldEditLink).toEqual(false)
    //     expect(wrapper.vm.newLinkValue).toEqual("")
    // })

    // test.only("editing link is false", () => {
    //     console.log(wrapper.html())
    //     expect(wrapper.findComponent(SocialMediaEditItem).editingLink).toEqual(false)
    // })
});
