import { mount } from "./global";
import MockAdapter from "axios-mock-adapter";
import { getAxiosInstance } from "@/api/api";
import BusinessCard from "../../src/components/BusinessCard";

describe("BusinessCard component unit tests", () => {
    let mockAxios;

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
    });

    beforeEach(() => {
        // mocks general info required by this component
        mockAxios
            .onGet("/contact_book/get_social_media_sites/")
            .reply(200, MOCK_SOCIALS);
    });

    test("is a Vue instance", () => {
        const wrapper = mount(BusinessCard, {
            propsData: {
                contact: MOCK_CONTACT,
                theme: "granite-night",
            },
        });
        expect(wrapper.findComponent(BusinessCard)).toBeTruthy();
    });

    test("has correct primary email", () => {
        const wrapper = mount(BusinessCard, {
            propsData: {
                contact: MOCK_CONTACT,
                theme: "granite-night",
            },
        });
        expect(wrapper.vm.primaryEmail).toEqual(MOCK_EMAILS[0].email_address);
    });

    test("has null primary email when contact contains no emails", () => {
        MOCK_CONTACT.emails = [];
        const wrapper = mount(BusinessCard, {
            propsData: {
                contact: MOCK_CONTACT,
                theme: "granite-night",
            },
        });
        expect(wrapper.vm.primaryEmail).toBe("");
    });
});
