<template>
    <div :class="{ 'edit-contacts': true, expanded: expanded }">
        <transition mode="out-in" name="fade">
            <div v-if="contact === null" class="hero is-fullheight is-relative">
                <div class="hero-body">
                    <div class="is-flex-grow-1">
                        <p
                            class="
                                subtitle
                                has-text-grey-light has-text-centered
                            "
                        >
                            Loading Contact
                        </p>
                        <progress class="progress is-small is-info" max="100">
                            15%
                        </progress>
                    </div>
                </div>
            </div>
            <div v-else class="is-relative">
                <div class="level top-header">
                    <div class="level-left">
                        <o-button
                            icon-left="times"
                            variant="light"
                            class="m-3"
                            @click="$router.push('/app/contacts')"
                        />
                        <h2 class="title p-3">
                            <span v-if="fullName">{{ fullName }}</span>
                            <span v-else>Add Contact</span>
                        </h2>
                    </div>
                    <div class="level-right">
                        <o-button variant="primary" @click="submit">
                            <span v-if="contact.id">Save contact</span>
                            <span v-else>Save new contact</span>
                        </o-button>
                    </div>
                </div>

                <div class="p-4">
                    <!--                    <div class="box m-3">-->
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

                    <o-collapse v-model:open="extraNameOpen" animation="slide">
                        <template #trigger="props">
                            <div class="is-flex">
                                <!--                                <div class="card-header" role="button">-->
                                <p class="is-flex-grow-1">
                                    <span v-if="props.open">Hide</span>
                                    <span v-else>Show</span>
                                    nickname, pronunciation, pronouns...
                                </p>
                                <a>
                                    <o-icon
                                        :icon="
                                            props.open
                                                ? 'caret-up'
                                                : 'caret-down'
                                        "
                                    />
                                </a>
                                <!--                                </div>-->
                            </div>
                        </template>
                        <div class="expanded-box">
                            <ValidatedField
                                v-model="model"
                                label="Nickname"
                                name="nickname"
                                :server-data="serverData"
                                placeholder="Enter a nickname"
                            />
                            <ValidatedField
                                v-model="model"
                                label="Name Pronunciation"
                                name="name_pronunciation"
                                :server-data="serverData"
                                placeholder="Name pronunciation"
                            />
                            <ValidatedField
                                v-slot="{ value, setValue }"
                                v-model="model"
                                label="Pronouns"
                                name="pronouns"
                                :server-data="serverData"
                            >
                                <o-select
                                    :model-value="value"
                                    placeholder="..."
                                    @update:model-value="setValue"
                                >
                                    <option value=""></option>
                                    <option value="she/her">she/her</option>
                                    <option value="he/him">he/him</option>
                                    <option value="they/them">they/them</option>
                                </o-select>
                            </ValidatedField>
                            <ValidatedField
                                v-model="model"
                                label="Title"
                                name="title"
                                :server-data="serverData"
                                placeholder="e.g.: Mr, Mrs, Dr"
                            ></ValidatedField>
                        </div>
                    </o-collapse>

                    <hr />

                    <ValidatedField
                        v-model="model"
                        name="job_title"
                        label="Job Title"
                        :server-data="serverData"
                        placeholder="e.g. Software Developer"
                    />

                    <o-field grouped>
                        <ValidatedField
                            v-model="model"
                            name="department"
                            label="Department"
                            :server-data="serverData"
                            placeholder="e.g.: Middle Office"
                        >
                        </ValidatedField>

                        <ValidatedField
                            v-model="model"
                            name="company"
                            label="Company"
                            :server-data="serverData"
                            placeholder="e.g.: Pied Piper"
                        >
                        </ValidatedField>
                    </o-field>

                    <hr />

                    <ValidatedField
                        v-model="model"
                        name="side_notes"
                        label="Side Notes"
                        :server-data="serverData"
                        placeholder="Take notes about this person here to remember for next time."
                        type="textarea"
                    >
                    </ValidatedField>

                    <ValidatedField
                        v-slot="{ value, setValue }"
                        v-model="model"
                        name="regularity_of_contact"
                        label="How often to keep in touch"
                        :server-data="serverData"
                    >
                        <o-select
                            :model-value="value"
                            @update:model-value="setValue"
                        >
                            <option value="104">Twice a week</option>
                            <option value="52">Weekly</option>
                            <option value="26">Fortnightly</option>
                            <option value="12">Monthly</option>
                            <option value="6">Every two months</option>
                            <option value="2">Twice a year</option>
                            <option value="1">Once a year</option>
                        </o-select>
                    </ValidatedField>

                    <!--                    <o-field label="Last Time Contacted">-->
                    <!--                        <o-datepicker-->
                    <!--                            placeholder="select last time contacted"-->
                    <!--                            icon="calendar"-->
                    <!--                            trap-focus-->
                    <!--                        />-->
                    <!--                    </o-field>-->

                    <hr />

                    <div class="notification">
                        <strong>Please note:</strong> email addresses, phone
                        numbers and social media links are currently not
                        persisted to the database.
                    </div>

                    <p id="email-subtitle" class="subtitle">Email Address</p>

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
                <!--                    </div>-->
            </div>
        </transition>

        <o-modal :active="isDiscardChangesDialogActive" width="400">
            <div class="modal-card">
                <div class="modal-card-head">
                    <div class="modal-card-title">Discard changes</div>
                </div>
                <div class="modal-card-body">
                    <p>
                        Are you sure you want to discard changes to this
                        contact?
                    </p>
                </div>
                <div class="modal-card-foot">
                    <button
                        class="button is-primary"
                        @click="$emit('discard-changes')"
                    >
                        Discard changes
                    </button>
                    <button class="button" @click="$emit('cancel-discard')">
                        Cancel
                    </button>
                </div>
            </div>
        </o-modal>
    </div>
</template>

<script lang="ts">
import { Contact, getFullName } from "@/api/contacts";
import { Options, prop, Vue } from "vue-class-component";
import ValidatedField from "@/components/ValidatedField.vue";
import { getAxiosInstance, ServerData } from "@/api/api";
import { PropType } from "vue";
import { defaultToast } from "@/toasts";
import { deepCopy } from "@/api/utils";

class Props {
    contact = prop({
        type: Object as PropType<Contact | null>,
        default: null,
    });
    expanded!: boolean;
    isDiscardChangesDialogActive!: boolean;
}

@Options({
    components: { ValidatedField },
    watch: {
        contact: "setModel",
    },
    emits: ["discard-changes", "cancel-discard"],
})
export default class ContactsEdit extends Vue.with(Props) {
    socials = [];
    emails = [];
    phones = [];

    model: Contact = new Contact();
    serverData = new ServerData(new Contact());

    extraNameOpen = false;

    get fullName() {
        return getFullName(this.model);
    }

    setModel() {
        if (this.contact !== null) {
            this.model = deepCopy(this.contact);
            this.serverData = new ServerData(this.contact);
        }
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
            let response = await getAxiosInstance().request({
                url:
                    "contact_book/" +
                    (this.model.id
                        ? "update_contact_by_id/" + this.model.id
                        : "create_contact"),
                method: this.model.id ? "PUT" : "POST",
                data: this.model,
            });

            this.$emit("refresh-contacts");

            if (response.status === 201) {
                this.$oruga.notification.open(
                    defaultToast("success", "Contact created")
                );
                this.serverData.captureServerResponse(response.data);
                this.model = deepCopy(response.data);
                await this.$router.push("/app/contacts/" + response.data.id);
            } else {
                this.serverData.captureServerResponse(deepCopy(this.model));
                this.$oruga.notification.open(
                    defaultToast("info", "Contact updated")
                );
            }
        } catch (e) {
            this.serverData.captureServerResponse(deepCopy(this.model), e);
        }
    }
    hasUnsavedChanges(): boolean {
        if (this.contact === null) {
            return false;
        }
        return !this.serverData.matchesClientModel(this.model);
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

.expanded-box {
    margin-top: 10px;
    padding-top: 20px;
    border-top: 1px solid #ccc;
}

.top-header {
    position: sticky;
    z-index: 10;
    top: 0;
    border-radius: 0;
    background-color: #fafafa;
    border-bottom: 1px solid #ccc;
}
</style>
