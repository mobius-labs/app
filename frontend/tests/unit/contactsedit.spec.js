import { mount } from "@vue/test-utils";
import ContactsEdit from "../../src/components/ContactsEdit.vue";

describe("ContactsEdit component unit tests", () => {
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
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: null,
            },
        });
        wrapper.find("o-button.floating-close-button").trigger("click");
        expect(wrapper.emitted("close").length).toBe(1);
    });

    test("Click contact to edit text is displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: null,
            },
        });
        expect(wrapper.find("hero is-fullheight is-relative")).toBeTruthy();
        expect(wrapper.html()).toContain("Please select a contact to edit.");
    });

    test("Close emitted when contact selected and close button clicked", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        wrapper.find("o-button.m-3").trigger("click");
        expect(wrapper.emitted("close").length).toBe(1);
    });

    test("Selected contact's name is displayed", () => {
        const contactName = "Shivanah";
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: contactName },
            },
        });
        expect(wrapper.find("is-relative")).toBeTruthy();
        expect(wrapper.html()).toContain(contactName);
        // expect(wrapper.find("h2.title p-3").text()).toBe(contactName);
    });

    test("First Name placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("[name = 'first_name']").attributes("placeholder")
        ).toBe("First Name");
    });

    test("Middle Name placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("[name = 'middle_name']").attributes("placeholder")
        ).toBe("Middle Name");
    });

    test("Surname placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("[name = 'surname']").attributes("placeholder")
        ).toBe("Surname");
    });

    // test.only("Extra contact details title displayed", () => {
    //     const wrapper = mount(ContactsEdit, {
    //         propsData: {
    //             expanded : true,
    //             contact: { name: 'contactName' },
    //         },
    //     });
    //     //expect(wrapper.find('.card-header-title').text()).toBe("Extra name details");
    //     expect(wrapper.html()).toContain("Extra name details");
    // });

    test("Nickname placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("[name = 'nickname']").attributes("placeholder")
        ).toBe("Enter a nickname");
    });

    test("Name Pronunciation placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("[name = 'pronunciation']").attributes("placeholder")
        ).toBe("Name pronunciation");
    });

    test("Pronouns placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("o-input[name = 'pronouns']").attributes("placeholder")
        ).toBe("e.g.: she/her");
    });

    test("Title field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("o-field[label='Title']").exists()).toBeTruthy();
    });

    test("Job Title field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("o-field[label='Job Title']").exists()
        ).toBeTruthy();
    });

    test("Department field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("o-field[label='Department']").exists()
        ).toBeTruthy();
    });

    test("Company field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("o-field[label='Company']").exists()).toBeTruthy();
    });

    test("Side Notes field exists", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(
            wrapper.find("o-field[label='Side Notes']").exists()
        ).toBeTruthy();
    });

    test("Datepicker placeholder displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("o-datepicker").attributes("placeholder")).toBe(
            "select last time contacted"
        );
    });

    test("Email heading displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("p.email-subtitle").text()).toBe("Email");
    });

    // test('Delete email function called when delete email button clicked', () => {
    //     const wrapper = mount(ContactsEdit, {
    //         propsData : {
    //             expanded : true,
    //             contact : {name: 'contactName'}
    //         }
    //     });
    //     wrapper.setData({emails: [('shiv@gmail.com', 0)]});
    //     const deleteEmail= jest.spyOn(ContactsEdit.methods, 'deleteEmail');
    //     // wrapper.find('o-button.delete-email').trigger('click');
    //     wrapper.find('o-button#delete-email').trigger('click');
    //     expect(deleteEmail).toHaveBeenCalled();
    // })

    test("Add email button displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("o-button.add-email").text()).toBe(
            "Add email address"
        );
    });

    test("Phone number heading displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("p.phone-subtitle").text()).toBe("Phone Numbers");
    });

    test("Add phone number button displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("o-button.add-phone").text()).toBe(
            "Add phone number"
        );
    });

    test("Social Media heading displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("p.social-subtitle").text()).toBe("Social Media");
    });

    test("Add social media button displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                expanded: true,
                contact: { name: "contactName" },
            },
        });
        expect(wrapper.find("o-button.add-social").text()).toBe(
            "Add social media"
        );
    });
});
