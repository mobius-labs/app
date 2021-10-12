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
                        data-test="close-button"
                        @click="$router.push('/app/contacts')"
                    />
                    <h2 class="title p-3">
                        <span v-if="fullName" data-test="contact-name">{{
                            fullName
                        }}</span>
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
                <div class="space-items">
                    <ValidatedField
                        :model="model"
                        name="first_name"
                        placeholder="First Name"
                        expanded
                    />
                    <ValidatedField
                        :model="model"
                        name="middle_name"
                        placeholder="Middle Name"
                        expanded
                    >
                    </ValidatedField>
                    <ValidatedField
                        :model="model"
                        name="surname"
                        placeholder="Surname"
                        expanded
                    >
                    </ValidatedField>
                </div>

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
                            name="nickname"
                            placeholder="Enter a nickname"
                        />
                        <ValidatedField
                            :model="model"
                            name="name_pronunciation"
                            placeholder="Add pronunciation notes here..."
                        />
                        <ValidatedField
                            v-slot="{ value, setValue }"
                            :model="model"
                            name="pronouns"
                        >
                            <o-select
                                :model-value="value"
                                ref="pronouns"
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
                            name="title"
                            placeholder="e.g.: Mr, Mrs, Dr"
                        ></ValidatedField>
                    </div>
                </o-collapse>

                <hr />

                <ContactsOneToMany
                    v-slot="{ model, updateItem, debounceUpdateItem }"
                    ref="emails"
                    add-button-text="Add Email Address"
                    title="Email Addresses"
                    :fresh-item="freshEmailAddress"
                    api-name="email"
                    :contact-id="contactId"
                    :skip-reload="skipReload"
                    @update:saving="(v) => (savingEmails = v)"
                >
                    <ValidatedField
                        v-slot="{ value, setValue }"
                        :label="null"
                        :model="model"
                        name="label"
                        :update-value="updateItem"
                        placeholder="Type"
                    >
                        <o-select
                            :model-value="value"
                            @update:model-value="setValue"
                        >
                            <option value="business">Business</option>
                            <option value="friend">Friend</option>
                            <option value="family">Family</option>
                            <option value="other">Other</option>
                        </o-select>
                    </ValidatedField>
                    <ValidatedField
                        :model="model"
                        name="email_address"
                        :label="null"
                        :update-value="debounceUpdateItem"
                        placeholder="e.g.: johndoe@gmail.com"
                        required
                    ></ValidatedField>
                </ContactsOneToMany>

                <ContactsOneToMany
                    v-slot="{ model, updateItem, debounceUpdateItem }"
                    ref="phoneNumbers"
                    add-button-text="Add Phone Number"
                    title="Phone Numbers"
                    :fresh-item="freshPhoneNumber"
                    api-name="phone_no"
                    :contact-id="contactId"
                    :skip-reload="skipReload"
                    @update:saving="(v) => (savingPhones = v)"
                >
                    <ValidatedField
                        v-slot="{ value, setValue }"
                        :label="null"
                        :model="model"
                        name="label"
                        :update-value="updateItem"
                        placeholder="Type"
                    >
                        <o-select
                            :model-value="value"
                            @update:model-value="setValue"
                        >
                            <option value="business">Business</option>
                            <option value="friend">Friend</option>
                            <option value="family">Family</option>
                            <option value="other">Other</option>
                        </o-select>
                    </ValidatedField>
                    <ValidatedField
                        :model="model"
                        name="number"
                        :label="null"
                        :update-value="debounceUpdateItem"
                        placeholder="enter a phone number"
                        required
                    ></ValidatedField>
                </ContactsOneToMany>

                <SocialMediaEdit
                    ref="socialMedia"
                    :contact-id="contactId"
                    :skip-reload="skipReload"
                    @update:saving="(v) => (savingSocials = v)"
                ></SocialMediaEdit>

                <ContactsOneToMany
                    v-slot="{ model, updateItem, debounceUpdateItem }"
                    ref="addresses"
                    add-button-text="Add Address"
                    title="Addresses"
                    :fresh-item="freshAddress"
                    api-name="address"
                    :contact-id="contactId"
                    :skip-reload="skipReload"
                    @update:saving="(v) => (savingAddresses = v)"
                >
                    <div class="has-background-white-ter p-3 mb-3">
                        <ValidatedField
                            :model="model"
                            name="address_line_one"
                            label="Address Line 1"
                            :update-value="debounceUpdateItem"
                            placeholder="Address Line 1"
                        ></ValidatedField>
                        <ValidatedField
                            :model="model"
                            name="address_line_two"
                            label="Address Line 2"
                            :update-value="debounceUpdateItem"
                            placeholder="Address Line 2"
                        ></ValidatedField>
                        <div class="space-items">
                            <ValidatedField
                                :model="model"
                                name="suburb"
                                :update-value="debounceUpdateItem"
                                placeholder="Suburb"
                            ></ValidatedField>
                            <ValidatedField
                                :model="model"
                                name="postcode"
                                :update-value="debounceUpdateItem"
                                placeholder="Postcode"
                            ></ValidatedField>
                            <ValidatedField
                                :model="model"
                                name="state"
                                :update-value="debounceUpdateItem"
                                placeholder="State"
                            ></ValidatedField>
                        </div>

                        <o-switch
                            :model-value="model.model.is_current"
                            class="mb-4"
                            @update:model-value="
                                (v) => updateItem({ is_current: v })
                            "
                            >Current Address?</o-switch
                        >

                        <o-switch
                            :model-value="model.model.is_hometown"
                            class="mb-4"
                            @update:model-value="
                                (v) => updateItem({ is_hometown: v })
                            "
                            >Is Hometown?</o-switch
                        >
                    </div>
                </ContactsOneToMany>

                <ImportantDatesEdit
                    ref="importantDates"
                    :contact-id="contactId"
                    :skip-reload="skipReload"
                    @update:saving="(v) => (savingImportantDates = v)"
                ></ImportantDatesEdit>

                <hr />

                <ValidatedField
                    :model="model"
                    name="job_title"
                    placeholder="e.g. Software Developer"
                />

                <o-field grouped>
                    <ValidatedField
                        :model="model"
                        name="department"
                        placeholder="e.g.: Middle Office"
                    >
                    </ValidatedField>
                    <ValidatedField
                        :model="model"
                        name="company"
                        placeholder="e.g.: Pied Piper"
                    >
                    </ValidatedField>
                </o-field>

                <hr />

                <ValidatedField
                    :model="model"
                    name="side_notes"
                    data-test="side_notes"
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
                <!--       -->
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
import { getAxiosInstance } from "@/api/api";
import { defaultToast } from "@/toasts";
import ContactsOneToMany from "@/components/ContactsOneToMany.vue";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";
import NonFieldErrorsList from "@/components/NonFieldErrorsList.vue";
import SocialMediaEdit from "@/components/SocialMediaEdit.vue";
import ImportantDatesEdit from "@/components/ImportantDatesEdit.vue";
import { Model } from "@/api/model";

class Props {
    contactId!: number | null;
    expanded!: boolean;
    isDiscardChangesDialogActive!: boolean;
}

@Options({
    components: {
        SocialMediaEdit,
        NonFieldErrorsList,
        SpinnerOverlay,
        ContactsOneToMany,
        ValidatedField,
        ImportantDatesEdit,
    },
    watch: { contactId: "onContactIdUpdated", saving: "onSavingUpdated" },
    emits: ["discard-changes", "cancel-discard", "contact-updated"],
})
export default class ContactsEdit extends Vue.with(Props) {
    model = new Model<Contact>(new Contact());

    extraNameOpen = false;
    savingEmails = false;
    savingPhones = false;
    savingAddresses = false;
    savingSocials = false;
    savingImportantDates = false;
    loading = false;

    // There is a tricky edge case, whereby we fill out a valid contact, but
    // with invalid email/phone/social/address, and then click "create contact".
    // POSTing the contact will succeed, but POSTing the email/phone will not.
    // We need to navigate the user to the contacts "edit" URL, but keep the
    // email/phone/social/address which has failed validation, so the user can fix it.
    skipReloadForId: number | null = null;

    get saving() {
        return (
            this.model.isSubmitting ||
            this.savingEmails ||
            this.savingPhones ||
            this.savingAddresses ||
            this.savingSocials ||
            this.savingImportantDates
        );
    }

    get fullName() {
        if (!this.model) {
            return null;
        }
        return getFullName(this.model.model as Contact);
    }

    onSavingUpdated(newVal: boolean, oldVal: boolean) {
        if (!newVal && oldVal && this.model.model.id) {
            // if `saving` switched from `true` to `false`, then the contact has just been updated
            this.$emit("contact-updated", this.model.model);
        }
    }

    skipReload(id: number | null) {
        return id !== null && id === this.skipReloadForId;
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

            if (response.status === 201) {
                this.$oruga.notification.open(
                    defaultToast("info", "Contact created")
                );
                this.model.captureServerResponse(response.data);
                // keep around any phones/emails/socials which the user added,
                // rather than reloading them from scratch
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
            (this.$refs.emails as ContactsOneToMany).hasUnsavedChanges() ||
            (this.$refs.addresses as ContactsOneToMany).hasUnsavedChanges() ||
            (this.$refs.socialMedia as SocialMediaEdit).hasUnsavedChanges() ||
            (
                this.$refs.importantDates as ImportantDatesEdit
            ).hasUnsavedChanges()
        );
    }
    freshEmailAddress(): Record<string, any> {
        return { label: "other", email_address: "" };
    }
    freshPhoneNumber(): Record<string, any> {
        return { label: "other", number: "" };
    }
    freshAddress(): Record<string, any> {
        return { is_current: true };
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

.space-items {
    display: flex;
}

/* TODO: make this code cleaner */
:deep(.space-items > *:not(:last-child)) {
    margin-right: 0.5rem;
}
</style>
