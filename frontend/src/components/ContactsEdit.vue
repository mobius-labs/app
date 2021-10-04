<template>
    <div :class="'edit-contacts' + (expanded ? ' expanded' : '')">
        <transition mode="out-in">
            <div v-if="contact === null" class="hero is-fullheight is-relative">
                <o-button
                    icon-left="times"
                    class="floating-close-button"
                    variant="light"
                    @click="$emit('close')"
                />
                <div class="hero-body">
                    <div class="is-flex-grow-1">
                        <p
                            class="
                                subtitle
                                has-text-grey-light has-text-centered
                            "
                        >
                            Please select a contact to edit.
                        </p>
                    </div>
                </div>
            </div>
            <div v-else class="is-relative">
                <div class="level">
                    <div class="level-left">
                        <o-button
                            icon-left="times"
                            variant="light"
                            class="m-3"
                            @click="$emit('close')"
                        />
                        <h2 class="title p-3">
                            <span v-if="fullName">{{ fullName }}</span>
                            <span v-else>New Contact</span>
                        </h2>
                    </div>
                </div>

                <div class="box m-3">
                    <o-field grouped>
                        <ValidatedField
                            v-model="model"
                            label="First Name"
                            name="first_name"
                            :server-data="serverData"
                            expanded
                        />
                        <ValidatedField
                            v-model="model"
                            label="Middle Name"
                            name="middle_name"
                            :server-data="serverData"
                            expanded
                        >
                        </ValidatedField>
                        <ValidatedField
                            v-model="model"
                            label="Surname"
                            name="surname"
                            :server-data="serverData"
                            expanded
                        >
                        </ValidatedField>
                    </o-field>

                    <o-collapse animation="slide">
                        <template #trigger="props">
                            <div class="card-header" role="button">
                                <p class="card-header-title">
                                    Extra name details
                                </p>
                                <a class="card-header-icon">
                                    <o-icon
                                        :icon="
                                            props.open
                                                ? 'caret-up'
                                                : 'caret-down'
                                        "
                                    />
                                </a>
                            </div>
                        </template>
                        <div class="card-content no-padding">
                            <ValidatedField
                                v-model="model"
                                label="Nickname"
                                name="nickname"
                                :server-data="serverData"
                                placeholder="Enter a nickname"
                            ></ValidatedField>
                            <ValidatedField
                                v-model="model"
                                label="Name Pronunciation"
                                name="nickname"
                                :server-data="serverData"
                                placeholder="Name pronunciation"
                            ></ValidatedField>
                            <o-field label="Pronouns">
                                <o-input
                                    name="pronouns"
                                    placeholder="e.g.: she/her"
                                />
                            </o-field>
                            <o-field label="Title">
                                <o-input name="title" placeholder="" />
                            </o-field>
                        </div>
                    </o-collapse>

                    <hr />

                    <o-field label="Job Title">
                        <o-input name="job_title" placeholder="" />
                    </o-field>

                    <o-field grouped>
                        <o-field label="Department">
                            <o-input
                                name="department"
                                expanded
                                placeholder=""
                            />
                        </o-field>

                        <o-field label="Company">
                            <o-input name="company" expanded placeholder="" />
                        </o-field>
                    </o-field>

                    <hr />

                    <o-field label="Side Notes">
                        <o-input type="textarea" style="height: 5rem" />
                    </o-field>

                    <o-field label="Last Time Contacted">
                        <o-datepicker
                            placeholder="select last time contacted"
                            icon="calendar"
                            trap-focus
                        />
                    </o-field>

                    <o-button @click="submit">Save</o-button>

                    <hr />

                    <p id="email-subtitle" class="subtitle">Email</p>

                    <o-field
                        v-for="(email, i) in emails"
                        :key="i"
                        class="edit-email"
                    >
                        <o-select placeholder="Type">
                            <option value="home">Home</option>
                            <option value="work">Work</option>
                            <option value="school">School</option>
                        </o-select>

                        <o-input placeholder="Email address" required>{{
                            email.address
                        }}</o-input>
                        <o-button
                            id="delete-email"
                            icon-left="times"
                            @click="deleteEmail(i)"
                        ></o-button>
                    </o-field>

                    <o-button
                        class="add-email"
                        variant="success"
                        @click="emails.push({})"
                        >Add email address</o-button
                    >

                    <br />
                    <br />

                    <p id="phone-subtitle" class="subtitle">Phone Numbers</p>

                    <o-field v-for="(phone, i) in phones" :key="i">
                        <o-select placeholder="Type">
                            <option value="home">Home</option>
                            <option value="work">Work</option>
                            <option value="school">School</option>
                        </o-select>

                        <o-input placeholder="Email address" required>{{
                            phone.number
                        }}</o-input>
                        <button
                            class="delete-phone"
                            @click="deletePhone(i)"
                        ></button>
                    </o-field>

                    <o-button
                        class="add-phone"
                        variant="success"
                        @click="phones.push({})"
                        >Add phone number</o-button
                    >

                    <hr />

                    <p id="social-subtitle" class="subtitle">Social Media</p>

                    <o-field v-for="(social, i) in socials" :key="social.name">
                        <o-select placeholder="Select a social media">
                            <option value="facebook">Facebook</option>
                            <option value="twitter">Twitter</option>
                            <option value="instagram">Instagram</option>
                        </o-select>
                        <o-input
                            placeholder="Enter social media profile here..."
                            required
                            >{{ social.name }}</o-input
                        >

                        <button
                            class="delete-social"
                            @click="deleteSocial(i)"
                        ></button>
                    </o-field>

                    <o-button
                        class="add-social"
                        variant="success"
                        @click="socials.push({})"
                        >Add social media</o-button
                    >
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts">
import { Contact, getFullName } from "@/api/contacts";
import { Options, Vue } from "vue-class-component";
import ValidatedField from "@/components/ValidatedField.vue";
import { getAxiosInstance, ServerData } from "@/api/api";

class Props {
    contact: Object | null = null;
    expanded!: boolean;
}

@Options({
    components: { ValidatedField },
    watch: {
        contact: "setModel",
    },
    props: {
        expanded: { type: Boolean, required: true },
        contact: { type: Object, default: null },
    },
    emits: ["close"],
})
export default class ContactsEdit extends Vue.with(Props) {
    socials = [];
    emails = [];
    phones = [];

    model: Contact = new Contact();
    serverData = new ServerData();

    get fullName() {
        return getFullName(this.model);
    }

    setModel() {
        console.log(this.contact, this.expanded);
        this.model = JSON.parse(JSON.stringify(this.contact));
    }

    deleteSocial(index: number) {
        this.socials.splice(index, 1);
    }
    deleteEmail(index: number) {
        this.emails.splice(index, 1);
    }
    deletePhone(index: number) {
        this.phones.splice(index, 1);
    }

    async submit() {
        try {
            let response;
            if (this.model.id) {
                response = await getAxiosInstance().put(
                    "contact_book/update_contact_by_id/" + this.model.id,
                    this.model
                );
            } else {
                response = await getAxiosInstance().post(
                    "contact_book/create_contact",
                    this.model
                );
            }
            console.log(response);
        } catch (e) {
            this.serverData.handleError(e, this.model);
        }
    }
}
</script>

<style scoped>
.edit-contacts {
    overflow-y: auto;
    width: 0;
    flex: 0;
    transition: width 0.2s ease, flex 0.2s ease;
    border-left: 1px solid #ccc;
}

.expanded {
    min-width: 30rem;
    flex: 1;
}

.floating-close-button {
    position: absolute;
    top: 1rem;
    left: 1rem;
}

.no-padding {
    padding-left: 0;
    padding-right: 0;
}
</style>
