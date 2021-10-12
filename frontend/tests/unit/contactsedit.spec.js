import ContactsEdit from "../../src/components/ContactsEdit.vue";
import { mount } from "./global";
import MockAdapter from "axios-mock-adapter";
import { getAxiosInstance } from "@/api/api";
import { flushPromises } from "@vue/test-utils";
import ContactsOneToMany from "../../src/components/ContactsOneToMany.vue";

describe("ContactsEdit component unit tests", () => {
    let mockAxios;

    // an example mock contact object to use
    const MOCK_CONTACT = {
        id: 33,
        first_name: "Shivanah",
    };

    const MOCK_EMAILS = [
        {
            id: 39,
            address: "Foo@Bar.com",
            label: "family",
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
        mockAxios.onGet("/contact_book/get_social_media_sites/").reply(200, {});
        mockAxios
            .onGet("/contact_book/get_important_date_types/")
            .reply(200, {});
        // mocks requests for contact #33 (referred to in subsequent tests)
        mockAxios
            .onGet(`/contact_book/get_contact_by_id/33`)
            .reply(200, MOCK_CONTACT);
        mockAxios
            .onGet(`/contact_book/get_emails_by_cid/33`)
            .reply(200, MOCK_EMAILS);
        mockAxios.onGet(`/contact_book/get_phone_nos_by_cid/33`).reply(200, {});
        mockAxios.onGet(`/contact_book/get_addresss_by_cid/33`).reply(200, {});
        mockAxios
            .onGet(`/contact_book/get_important_dates_by_cid/33`)
            .reply(200, {});
        mockAxios
            .onGet(`/contact_book/get_social_media_contacts_by_cid/33`)
            .reply(200, {});
    });

    afterEach(() => {
        // resets the requests we handle
        mockAxios.reset();
    });

    test("is a Vue instance", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: null,
            },
        });
        expect(wrapper.findComponent(ContactsEdit)).toBeTruthy();
    });

    test("Close emitted when contact unselected and close button clicked", () => {
        const mockRouter = {
            push: jest.fn(),
        };
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: null,
            },
            global: {
                mocks: { $router: mockRouter },
            },
        });
        wrapper.get("[data-test='close-button']").trigger("click");
        expect(mockRouter.push).toHaveBeenCalledTimes(1);
        // upon close, we expect to be navigated to this URL
        expect(mockRouter.push).toHaveBeenCalledWith("/app/contacts");
    });

    // test("Click contact to edit text is displayed", () => {
    //     const wrapper = mount(ContactsEdit, {
    //         propsData: {
    //             expanded: true,
    //             contact: null,
    //         }
    //     });
    //     expect(wrapper.find("hero is-fullheight is-relative")).toBeTruthy();
    //     expect(wrapper.html()).toContain("Please select a contact to edit.");
    // });

    test("Close emitted when contact selected and close button clicked", () => {
        const mockRouter = {
            push: jest.fn(),
        };

        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: 33,
            },
            global: {
                mocks: { $router: mockRouter },
            },
        });
        wrapper.find("[data-test='close-button']").trigger("click");
        expect(mockRouter.push).toHaveBeenCalledTimes(1);
        expect(mockRouter.push).toHaveBeenCalledWith("/app/contacts");
    });

    test("Selected contact's name is displayed", async () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: 33,
            },
        });

        await flushPromises();

        expect(wrapper.find('[data-test="contact-name"]').text()).toBe(
            MOCK_CONTACT.first_name
        );
    });

    test("First Name placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(
            wrapper.find("input[name='first_name']").attributes("placeholder")
        ).toBe("First Name");
    });

    test("Middle Name placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(
            wrapper.find("input[name='middle_name']").attributes("placeholder")
        ).toBe("Middle Name");
    });

    test("Surname placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(
            wrapper.find("input[name='surname']").attributes("placeholder")
        ).toBe("Surname");
    });

    test("Extra contact details title displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(wrapper.text()).toContain(
            "Show nickname, pronunciation, pronouns..."
        );
    });

    test("Nickname placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(
            wrapper.find("input[name='nickname']").attributes("placeholder")
        ).toBe("Enter a nickname");
    });

    test("Name Pronunciation placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(
            wrapper
                .find('input[name="name_pronunciation"]')
                .attributes("placeholder")
        ).toContain("pronunciation");
    });

    test("Pronouns placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(
            wrapper.findComponent({ ref: "pronouns" }).props("placeholder")
        ).toBe("...");
    });

    test("Title field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(wrapper.find("input[name='title']").exists()).toBeTruthy();
    });

    test("Job Title field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(wrapper.find("input[name='job_title']").exists()).toBeTruthy();
    });

    test("Department field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(wrapper.find("input[name='department']").exists()).toBeTruthy();
    });

    test("Company field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(wrapper.find("input[name='company']").exists()).toBeTruthy();
    });

    test("Side Notes field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        expect(
            wrapper.find('textarea[name="side_notes"]').exists()
        ).toBeTruthy();
    });

    // TODO: re-enable this test once "last contacted" field is readded
    // test("Datepicker placeholder displayed", () => {
    //     const wrapper = mount(ContactsEdit, {
    //         propsData: {
    //             expanded: true,
    //             contact: null,
    //         }
    //     });
    //     expect(wrapper.find("o-datepicker").attributes("placeholder")).toBe(
    //         "select last time contacted"
    //     );
    // });

    test("Delete email function called when delete email button clicked", async () => {
        const deleteItem = jest.spyOn(ContactsOneToMany.methods, "deleteItem");

        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: 33,
            },
        });
        // wait for the contact to load
        await flushPromises();
        // expect this API to be called
        mockAxios
            .onDelete("/contact_book/delete_email_by_eid/39")
            .reply(200, {});
        // when the "delete" button is clicked
        wrapper
            .getComponent({ ref: "emails" })
            .get('[data-test="delete-button"]')
            .trigger("click");
        await flushPromises();

        expect(deleteItem).toHaveBeenCalledWith(39);
        // expect one DELETE request
        expect(mockAxios.history.delete.length).toBe(1);
    });

    test("One to many titles and buttons displayed", async () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contactId: null,
            },
        });
        await flushPromises();
        for (let component of wrapper.findAllComponents(ContactsOneToMany)) {
            // check the title is as expected
            expect(component.find('[data-test="title"]').text()).toContain(
                component.props("title")
            );
            // check the button text is as expected
            expect(component.find('[data-test="add-button"]').text()).toContain(
                component.props("addButtonText")
            );
        }
    });

    // test.only("Display add and delete email actions upon clicking add email", () => {
    //     const wrapper = mount(ContactsEdit, {
    //         propsData: {
    //             expanded: true,
    //             contact: { name: "contactName" },
    //         },
    //     });
    //     wrapper.setData({emails: [({address: "shiv@gmail.com"}, 0)]});
    //     wrapper.find("o-button.add-email").trigger("click");
    //     //expect(wrapper.find("o-field.edit-email").exists()).toBeTruthy();
    // });
});
