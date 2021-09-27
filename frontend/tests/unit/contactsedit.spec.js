import { mount } from "@vue/test-utils";
import ContactsEdit from "../../src/components/ContactsEdit.vue";

describe("ContactsEdit component unit tests", () => {
    test("is a Vue instance", () => {
        const wrapper = mount(ContactsEdit);
        expect(wrapper.findComponent(ContactsEdit)).toBeTruthy();
    });

    test("Close emitted when contact unselected and close button clicked", () => {
        const wrapper = mount(ContactsEdit);
        wrapper.find("o-button.floating-close-button").trigger("click");
        expect(wrapper.emitted("close").length).toBe(1);
    });

    test("Click contact to edit text is displayed", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
                contact: null,
            },
        });
        expect(wrapper.find("hero is-fullheight is-relative")).toBeTruthy();
        expect(wrapper.html()).toContain("Please select a contact to edit.");
    });

    test("Close emitted when contact selected and close button clicked", () => {
        const wrapper = mount(ContactsEdit, {
            propsData: {
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
                contact: { name: contactName },
            },
        });
        expect(wrapper.find("is-relative")).toBeTruthy();
        expect(wrapper.html()).toContain(contactName);
        // expect(wrapper.find("h2.title p-3").text()).toBe(contactName);
    });

    // test('Delete email function called when delete email button clicked', () => {
    //     const wrapper = mount(ContactsEdit, {
    //         propsData : {
    //             contact : {name: 'contactName'}
    //         }
    //     });
    //     wrapper.setData({emails: [('shiv@gmail.com', 0)]});
    //     const deleteEmail= jest.spyOn(ContactsEdit.methods, 'deleteEmail');
    //     // wrapper.find('o-button.delete-email').trigger('click');
    //     wrapper.find('o-button#delete-email').trigger('click');
    //     expect(deleteEmail).toHaveBeenCalled();
    // })
});
