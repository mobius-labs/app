<template>
    <div :class="'edit-contacts' + (expanded ? ' expanded' : '')">
        <transition mode="out-in">
            <div v-if="contact === null" class="hero is-fullheight is-relative">
                <o-button
                    icon-left="times"
                    class="floating-close-button"
                    variant="light"
                    @click="$emit('close')"
                ></o-button>
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
                        ></o-button>
                        <h2 class="title p-3">{{ contact.name }}</h2>
                    </div>
                </div>

                <div class="box m-3">
                    <o-field grouped>
                        <o-field label="First Name">
                            <o-input
                                name="first_name"
                                placeholder="First Name"
                                expanded
                            ></o-input>
                        </o-field>
                        <o-field label="Middle Name">
                            <o-input
                                name="middle_name"
                                placeholder="Middle Name"
                                expanded
                            ></o-input>
                        </o-field>
                        <o-field label="Surname">
                            <o-input
                                name="surname"
                                placeholder="Surname"
                                expanded
                            ></o-input>
                        </o-field>
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
                                    >
                                    </o-icon>
                                </a>
                            </div>
                        </template>
                        <div class="card-content no-padding">
                            <o-field label="Nickname">
                                <o-input
                                    name="nickname"
                                    placeholder="Enter a nickname"
                                ></o-input>
                            </o-field>
                            <o-field label="Name Pronunciation">
                                <o-input
                                    name="pronunciation"
                                    placeholder="Name pronunciation"
                                ></o-input>
                            </o-field>
                            <o-field label="Pronouns">
                                <o-input
                                    name="pronouns"
                                    placeholder="e.g.: she/her"
                                ></o-input>
                            </o-field>
                            <o-field label="Title">
                                <o-input name="title" placeholder=""></o-input>
                            </o-field>
                        </div>
                    </o-collapse>

                    <hr />

                    <o-field label="Job Title">
                        <o-input name="job_title" placeholder=""></o-input>
                    </o-field>

                    <o-field grouped>
                        <o-field label="Department">
                            <o-input
                                name="department"
                                expanded
                                placeholder=""
                            ></o-input>
                        </o-field>

                        <o-field label="Company">
                            <o-input
                                name="company"
                                expanded
                                placeholder=""
                            ></o-input>
                        </o-field>
                    </o-field>

                    <hr />

                    <o-field label="Side Notes">
                        <o-input type="textarea" style="height: 5rem"></o-input>
                    </o-field>

                    <o-field label="Last Time Contacted">
                        <o-datepicker
                            placeholder="select last time contacted"
                            icon="calendar"
                            trap-focus
                        ></o-datepicker>
                    </o-field>

                    <hr />

                    <p id="email-subtitle" class="subtitle">Email</p>

                    <o-field
                        class="edit-email"
                        v-for="(email, i) in emails"
                        :key="i"
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
                            icon-left="times"
                            id="delete-email"
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

<script>
export default {
    name: "ContactsEdit",
    props: {
        expanded: {
            type: Boolean,
            required: true,
        },
        contact: {
            type: Object,
            default: null,
        },
    },
    emits: ["close"],
    data() {
        return {
            socials: [],
            emails: [],
            phones: [],
        };
    },
    methods: {
        deleteSocial(index) {
            this.socials.splice(index, 1);
        },
        deleteEmail(index) {
            this.emails.splice(index, 1);
        },
        deletePhone(index) {
            this.phones.splice(index, 1);
        },
    },
};
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
