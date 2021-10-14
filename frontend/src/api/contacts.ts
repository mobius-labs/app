// +ve if a proper server ID, -ve if just a local client ID for this editing session
export type ContactId = number;

// +ve if a proper server ID, null if doesn't exist on the server yet
export type ServerContactId = number | null;

// ms to wait before autosaving a contact
export const CONTACT_AUTOSAVE_TIMER_MS = 300;
export const CONTACTS_AUTOSAVE_REQUEST_MS = 700;

export class Contact {
    id: ServerContactId | null = null;
    title: string | null = null;
    first_name: string | null = null;
    middle_name: string | null = null;
    surname: string | null = null;
    company: string | null = "";
    job_title: string | null = "";
}

export interface Address {
    address_line_one: string;
    suburb: string;
}

export function getFullName(contact: Contact) {
    let s = "";
    if (contact.title) {
        s += contact.title + " ";
    }
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

export function concatAddress(address: Address) {
    return (
        address.address_line_one + (address.suburb ? ", " + address.suburb : "")
    );
}

export function displayRegularity(r: number) {
    if (r === 104) {
        return "Twice a week";
    } else if (r === 52) {
        return "Weekly";
    } else if (r === 26) {
        return "Fortnightly";
    } else if (r === 12) {
        return "Monthly";
    } else if (r === 6) {
        return "Every 2 months";
    } else if (r === 2) {
        return "Twice a year";
    } else if (r === 1) {
        return "Once a year";
    } else if (!r) {
        return null;
    } else {
        return "unknown";
    }
}
