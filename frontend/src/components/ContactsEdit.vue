<template>
    <transition-group mode="out-in" name="fade">
        <div
            v-show="loading"
            key="loading"
            class="hero is-fullheight is-relative"
        >
            <div class="hero-body">
                <div class="is-flex-grow-1">
                    <p class="subtitle has-text-grey-light has-text-centered">
                        Loading Contact
                    </p>
                    <progress
                        class="progress is-small is-info"
                        max="100"
                    ></progress>
                </div>
            </div>
        </div>

        <div v-show="!loading" key="main" class="is-relative">
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
                    <o-button
                        variant="primary"
                        :disabled="saving"
                        @click="submit"
                    >
                        <SpinnerOverlay :active="saving">
                            <span v-if="contactId">Save contact</span>
                            <span v-else>Save new contact</span>
                        </SpinnerOverlay>
                    </o-button>
                </div>
            </div>

            <div class="p-4">
                <o-field grouped>
                    <ValidatedField
                        :model="model"
                        label="First Name"
                        name="first_name"
                        expanded
                    />
                    <ValidatedField
                        :model="model"
                        label="Middle Name"
                        name="middle_name"
                        expanded
                    >
                    </ValidatedField>
                    <ValidatedField
                        :model="model"
                        label="Surname"
                        name="surname"
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
                                        props.open ? 'caret-up' : 'caret-down'
                                    "
                                />
                            </a>
                            <!--                                </div>-->
                        </div>
                    </template>
                    <div class="expanded-box">
                        <ValidatedField
                            :model="model"
                            label="Nickname"
                            name="nickname"
                            placeholder="Enter a nickname"
                        />
                        <ValidatedField
                            :model="model"
                            label="Name Pronunciation"
                            name="name_pronunciation"
                            placeholder="Name pronunciation"
                        />
                        <ValidatedField
                            v-slot="{ value, setValue }"
                            :model="model"
                            label="Pronouns"
                            name="pronouns"
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
                            :model="model"
                            label="Title"
                            name="title"
                            placeholder="e.g.: Mr, Mrs, Dr"
                        ></ValidatedField>
                    </div>
                </o-collapse>

                <hr />

                <ValidatedField
                    :model="model"
                    name="job_title"
                    label="Job Title"
                    placeholder="e.g. Software Developer"
                />

                <o-field grouped>
                    <ValidatedField
                        :model="model"
                        name="department"
                        label="Department"
                        placeholder="e.g.: Middle Office"
                    >
                    </ValidatedField>

                    <ValidatedField
                        :model="model"
                        name="company"
                        label="Company"
                        placeholder="e.g.: Pied Piper"
                    >
                    </ValidatedField>
                </o-field>

                <hr />

                <ValidatedField
                    :model="model"
                    name="side_notes"
                    label="Side Notes"
                    placeholder="Take notes about this person here to remember for next time."
                    type="textarea"
                >
                </ValidatedField>

                <ValidatedField
                    v-slot="{ value, setValue }"
                    :model="model"
                    name="regularity_of_contact"
                    label="How often to keep in touch"
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

                <ContactsOneToMany
                    v-slot="{
                        model,
                        updateItem,
                        deleteItem,
                        debounceUpdateItem,
                    }"
                    ref="emails"
                    add-button-text="Add Email Address"
                    title="Email Addresses"
                    :fresh-item="freshEmailAddress"
                    api-name="email"
                    :contact-id="contactId"
                    :skip-reload="skipReload"
                    @update:saving="(v) => (savingEmails = v)"
                >
                    <o-field
                        :variant="
                            model.hasErrorsForField('label') ||
                            model.nonFieldErrors.length > 0
                                ? 'danger'
                                : null
                        "
                        :message="model.displayFirstError('label')"
                    >
                        <o-select
                            placeholder="Type"
                            :model-value="model.model.label"
                            @update:model-value="
                                (v) => updateItem({ label: v })
                            "
                        >
                            <option value="business">Business</option>
                            <option value="friend">Friend</option>
                            <option value="family">Family</option>
                            <option value="other">Other</option>
                        </o-select>
                    </o-field>
                    <o-field
                        :variant="
                            model.hasErrorsForField('email_address') ||
                            model.nonFieldErrors.length > 0
                                ? 'danger'
                                : null
                        "
                        :message="model.displayFirstError('email_address')"
                        class="ml-2"
                    >
                        <o-input
                            placeholder="e.g.: johndoe@gmail.com"
                            required
                            :model-value="model.model.email_address"
                            @update:model-value="
                                (v) => debounceUpdateItem({ email_address: v })
                            "
                        ></o-input>
                    </o-field>
                    <button
                        class="delete mt-3 ml-2"
                        @click="deleteItem"
                    ></button>
                </ContactsOneToMany>

                <ContactsOneToMany
                    v-slot="{
                        model,
                        updateItem,
                        deleteItem,
                        debounceUpdateItem,
                    }"
                    ref="phoneNumbers"
                    add-button-text="Add Phone Number"
                    title="Phone Numbers"
                    :fresh-item="freshPhoneNumber"
                    api-name="phone_no"
                    :contact-id="contactId"
                    :skip-reload="skipReload"
                    @update:saving="(v) => (savingPhones = v)"
                >
                    <o-field
                        :variant="
                            model.hasErrorsForField('label') ||
                            model.nonFieldErrors.length > 0
                                ? 'danger'
                                : null
                        "
                        :message="model.displayFirstError('label')"
                    >
                        <o-select
                            placeholder="Type"
                            :model-value="model.model.label"
                            @update:model-value="
                                (v) => updateItem({ label: v })
                            "
                        >
                            <option value="business">Business</option>
                            <option value="friend">Friend</option>
                            <option value="family">Family</option>
                            <option value="other">Other</option>
                        </o-select>
                    </o-field>
                    <o-field
                        :variant="
                            model.hasErrorsForField('number') ||
                            model.nonFieldErrors.length > 0
                                ? 'danger'
                                : null
                        "
                        :message="model.displayFirstError('number')"
                        class="ml-2"
                    >
                        <o-input
                            placeholder="enter a phone number"
                            required
                            :model-value="model.model.number"
                            @update:model-value="
                                (v) => debounceUpdateItem({ number: v })
                            "
                        ></o-input>
                    </o-field>
                    <button
                        class="delete mt-3 ml-2"
                        @click="deleteItem"
                    ></button>
                </ContactsOneToMany>

                <ContactsOneToMany
                    v-slot="{
                        model,
                        updateItem,
                        deleteItem,
                        debounceUpdateItem,
                    }"
                    ref="addresses"
                    add-button-text="Add Address"
                    title="Addresses"
                    :fresh-item="freshAddress"
                    api-name="address"
                    :contact-id="contactId"
                    :skip-reload="skipReload"
                    @update:saving="(v) => (savingAddresses = v)"
                >
                    <div>
                        <o-field
                            :variant="
                                model.hasErrorsForField('address_line_one') ||
                                model.nonFieldErrors.length > 0
                                    ? 'danger'
                                    : null
                            "
                            :message="
                                model.displayFirstError('address_line_one')
                            "
                        >
                            <o-input
                                placeholder="address line one"
                                required
                                :model-value="model.model.address_line_one"
                                @update:model-value="
                                    (v) =>
                                        debounceUpdateItem({
                                            address_line_one: v,
                                        })
                                "
                            ></o-input>
                        </o-field>
                        <o-field
                            :variant="
                                model.hasErrorsForField('address_line_two') ||
                                model.nonFieldErrors.length > 0
                                    ? 'danger'
                                    : null
                            "
                            :message="
                                model.displayFirstError('address_line_two')
                            "
                        >
                            <o-input
                                placeholder="address line two"
                                required
                                :model-value="model.model.address_line_two"
                                @update:model-value="
                                    (v) =>
                                        debounceUpdateItem({
                                            address_line_two: v,
                                        })
                                "
                            ></o-input>
                        </o-field>

                        <o-field>
                            <o-field
                                :variant="
                                    model.hasErrorsForField('suburb') ||
                                    model.nonFieldErrors.length > 0
                                        ? 'danger'
                                        : null
                                "
                                :message="model.displayFirstError('suburb')"
                            >
                                <o-input
                                    placeholder="suburb"
                                    required
                                    :model-value="model.model.suburb"
                                    @update:model-value="
                                        (v) => debounceUpdateItem({ suburb: v })
                                    "
                                ></o-input>
                            </o-field>

                            <o-field
                                :variant="
                                    model.hasErrorsForField('postcode') ||
                                    model.nonFieldErrors.length > 0
                                        ? 'danger'
                                        : null
                                "
                                :message="model.displayFirstError('postcode')"
                            >
                                <o-input
                                    placeholder="postcode"
                                    required
                                    :model-value="model.model.postcode"
                                    @update:model-value="
                                        (v) =>
                                            debounceUpdateItem({ postcode: v })
                                    "
                                ></o-input>
                            </o-field>

                            <o-field
                                :variant="
                                    model.hasErrorsForField('state') ||
                                    model.nonFieldErrors.length > 0
                                        ? 'danger'
                                        : null
                                "
                                :message="model.displayFirstError('state')"
                            >
                                <o-input
                                    placeholder="state"
                                    required
                                    :model-value="model.model.state"
                                    @update:model-value="
                                        (v) => debounceUpdateItem({ state: v })
                                    "
                                ></o-input>
                            </o-field>
                        </o-field>

                        <o-switch
                            :model-value="model.model.is_current"
                            @update:model-value="
                                (v) => updateItem({ is_current: v })
                            "
                            class="mb-4"
                            >Current Address?</o-switch
                        >

                        <o-switch
                            :model-value="model.model.is_hometown"
                            @update:model-value="
                                (v) => updateItem({ is_hometown: v })
                            "
                            class="mb-4"
                            >Is Hometown?</o-switch
                        >
                    </div>
                    <button
                        class="delete mt-3 ml-2"
                        @click="deleteItem"
                    ></button>
                </ContactsOneToMany>
            </div>

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
    </transition-group>
</template>

<script lang="ts">
import { Contact, getFullName } from "@/api/contacts";
import { Options, Vue } from "vue-class-component";
import ValidatedField from "@/components/ValidatedField.vue";
import { getAxiosInstance, Model } from "@/api/api";
import { defaultToast } from "@/toasts";
import ContactsOneToMany from "@/components/ContactsOneToMany.vue";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";
import NonFieldErrorsList from "@/components/NonFieldErrorsList.vue";

class Props {
    contactId!: number | null;
    expanded!: boolean;
    isDiscardChangesDialogActive!: boolean;
}

@Options({
    components: {
        NonFieldErrorsList,
        SpinnerOverlay,
        ContactsOneToMany,
        ValidatedField,
    },
    watch: { contactId: "onContactIdUpdated" },
    emits: ["discard-changes", "cancel-discard", "refresh-contacts"],
})
export default class ContactsEdit extends Vue.with(Props) {
    model = new Model(new Contact());

    extraNameOpen = false;
    savingEmails = false;
    savingPhones = false;
    savingAddresses = false;
    loading = false;

    // There is a tricky edge case, whereby we fill out a valid contact, but
    // with invalid email/phone/social/address, and then click "create contact".
    // POSTing the contact will succeed, but POSTing the email/phone will not.
    // We need to navigate the user to the contacts "edit" URL, but keep the
    // email/phone/social/address which has failed validation, so the user can fix it.
    skipReloadForId: number | null = null;

    get saving() {
        return (
            this.model.isSubmitting || this.savingEmails || this.savingPhones
        );
    }

    get fullName() {
        if (!this.model) {
            return null;
        }
        return getFullName(this.model.model as Contact);
    }

    skipReload(id: number | null) {
        return id === this.skipReloadForId;
    }

    async onContactIdUpdated(newId: number | null) {
        if (!newId) {
            this.model = new Model(new Contact());
            return;
        }
        // on the next page change, clear this flag
        if (newId !== this.skipReloadForId) {
            this.skipReloadForId = null;
        } else if (newId === this.skipReloadForId) {
            console.log("skipping reload");
            return;
        }

        this.loading = true;
        let response = await getAxiosInstance().get(
            "contact_book/get_contact_by_id/" + this.contactId
        );
        this.model = new Model(response.data);
        this.loading = false;
    }

    async mounted() {
        await this.onContactIdUpdated(this.contactId);
    }

    async submit() {
        await this.model.tryUpdate(async () => {
            let response = await getAxiosInstance().request({
                url:
                    "contact_book/" +
                    (this.model.model.id
                        ? "update_contact_by_id/" + this.model.model.id
                        : "create_contact"),
                method: this.model.model.id ? "PUT" : "POST",
                data: this.model.model,
            });

            this.$emit("refresh-contacts");

            if (response.status === 201) {
                this.$oruga.notification.open(
                    defaultToast("success", "Contact created")
                );
                this.model.captureServerResponse(response.data);
                // keep around any phones/emails/socials which the user added,
                // so they get saved
                this.skipReloadForId = response.data.id;
                await this.$router.push("/app/contacts/" + response.data.id);
            } else {
                this.model.captureServerResponse(null);
                this.$oruga.notification.open(
                    defaultToast("info", "Contact updated")
                );
            }
        });
    }

    hasUnsavedChanges(): boolean {
        return (
            !this.model.matchesServer() ||
            (
                this.$refs.phoneNumbers as ContactsOneToMany
            ).hasUnsavedChanges() ||
            (this.$refs.emails as ContactsOneToMany).hasUnsavedChanges()
        );
    }
    freshEmailAddress(): Record<string, any> {
        return { label: "other", email_address: "" };
    }
    freshPhoneNumber(): Record<string, any> {
        return { label: "other", number: "" };
    }
    freshAddress(): Record<string, any> {
        return {};
    }
}
</script>

<style scoped>
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
