export class Contact {
    id: number | null = null;
    first_name = null;
    middle_name = null;
    surname = null;
}

export function getFullName(contact: Contact) {
    let s = "";
    if (contact.first_name) {
        s += contact.first_name + " ";
    }
    if (contact.middle_name) {
        s += contact.middle_name + " ";
    }
    if (contact.surname) {
        s += contact.surname;
    }
    return s;
}
