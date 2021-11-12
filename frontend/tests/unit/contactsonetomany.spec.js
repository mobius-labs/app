import { mount } from "./global";
import MockAdapter from "axios-mock-adapter";
import { getAxiosInstance } from "@/api/api";
import ContactsOneToMany from "../../src/components/ContactsOneToMany.vue";

describe("ContactsOneToMany component unit tests", () => {
    let mockAxios;
    let wrapper, wrapper_two;
    let add_spy, delete_spy, update_spy, inflight_spy;

    const MOCK_SOCIALS = [
        {
            id: 1,
            link: "shivshetty",
        },
        {
            id: 2,
            link: "shiv_shetty",
        },
    ];

    const FRESH_SOCIAL = () => {
        return {
            id: 3,
            link: "shiv.shetty",
        };
    };

    const OTM_PROPS = {
        title: "Social Media",
        addButtonText: "Add social media",
        initialItems: MOCK_SOCIALS,
        freshItem: FRESH_SOCIAL,
        serverId: 1,
        apiName: "social_media_contact",
    };

    const NO_SERVER_OTM_PROPS = {
        title: "Social Media",
        addButtonText: "Add social media",
        initialItems: MOCK_SOCIALS,
        freshItem: FRESH_SOCIAL,
        apiName: "social_media_contact",
    };

    beforeAll(() => {
        mockAxios = new MockAdapter(getAxiosInstance(), {
            onNoMatch: "throwException",
        });

        add_spy = jest.spyOn(ContactsOneToMany.methods, "addItem");
        delete_spy = jest.spyOn(ContactsOneToMany.methods, "deleteItem");
        update_spy = jest.spyOn(
            ContactsOneToMany.methods,
            "updateItemOnServer"
        );
        inflight_spy = jest.spyOn(
            ContactsOneToMany.methods,
            "markRequestAsInFlight"
        );

        wrapper = mount(ContactsOneToMany, {
            propsData: OTM_PROPS,
        });

        wrapper_two = mount(ContactsOneToMany, {
            propsData: NO_SERVER_OTM_PROPS,
        });
    });

    beforeEach(() => {
        mockAxios
            .onGet(`/contact_book/get_social_media_contacts_by_cid/33`)
            .reply(200, MOCK_SOCIALS);

        mockAxios
            .onPut(`/contact_book/update_social_media_contacts_by_sid/2`)
            .reply(200, { response: "success" });
    });

    afterEach(() => {
        // resets the requests we handle
        mockAxios.reset();
    });

    test("is a Vue instance", () => {
        expect(wrapper.findComponent(ContactsOneToMany)).toBeTruthy();
    });

    test("Social Media title displayed", () => {
        expect(wrapper.find('p[data-test="title"]').text()).toContain(
            OTM_PROPS.title
        );
    });

    test("Add social media button displayed", () => {
        expect(wrapper.find('button[data-test="add-button"]').text()).toContain(
            OTM_PROPS.addButtonText
        );
    });

    test("Add item  method called when add social media button clicked", () => {
        wrapper.find('button[data-test="add-button"]').trigger("click");

        expect(add_spy).toHaveBeenCalled();
    });

    test("Delete item method called when item deleted", () => {
        wrapper.find('button[data-test="delete-button"]').trigger("click");

        expect(delete_spy).toHaveBeenCalled();
    });

    // test("Delete item fails with invalid item id", () => {
    //     const deleteItem = wrapper.vm.deleteItem(22)
    //     expect(deleteItem).toBeUndefined()
    // })

    test("Update item method calls update on server and marks request as in flight", () => {
        wrapper.vm.updateItem(2, "shiv__shetty");
        expect(update_spy).toHaveBeenCalled();
        expect(inflight_spy).toHaveBeenCalled();
    });

    test("Update item on server fails if theres no server id", () => {
        const updated = wrapper_two.vm.updateItem(2, "shiv__shetty");
        expect(updated).toBe(undefined);
    });

    test("Update method fails with invalid item id", () => {
        const updatedItem = wrapper.vm.updateItem(22, "shiv__shetty");
        expect(updatedItem).toBe(undefined);
    });

    test("Has unsaved changes is false", () => {
        const unsavedChanges = wrapper.vm.hasUnsavedChanges();
        expect(unsavedChanges).toBeFalsy();
    });
});
