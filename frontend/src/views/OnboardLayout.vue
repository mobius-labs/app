<template>
    <section class="hero is-primary is-fullheight">
        <div class="hero-body column">
            <div class="box is-white has-content-centered welcome-box">
                <o-steps animated rounded custom-navigation>
                    <o-step-item icon="birthday-cake" step="1">
                        <div class="container has-text-centered">
                            <p class="title is-1 has-text-primary">
                                Congratulations on creating your account!
                            </p>
                            <p class="title is-4 has-text-primary">
                                Now, let's get to know you.
                            </p>
                        </div>
                    </o-step-item>
                    <o-step-item icon="user" step="2">
                        <div class="p-1 has-text-left">
                            <p class="title is-3 has-text-primary">
                                First, we'll cover the basics...
                            </p>
                        </div>
                        <div class="p-1">
                            <ValidatedField
                                label="Title"
                                :model="model"
                                name="title"
                                placeholder="Your title (Dr., Ms., Prof., Mr., etc.)"
                            />
                            <div class="space-items">
                                <ValidatedField
                                    label="First Name"
                                    :model="model"
                                    name="first_name"
                                    placeholder="Your first name"
                                />
                                <ValidatedField
                                    label="Middle Name"
                                    :model="model"
                                    name="middle_name"
                                    placeholder="Your middle name"
                                />
                                <ValidatedField
                                    label="Last Name"
                                    :model="model"
                                    name="last_name"
                                    placeholder="Your last name"
                                />
                            </div>
                            <ValidatedField
                                label="Pronouns (optional)"
                                :model="model"
                                name="pronouns"
                                placeholder="Your pronouns (She/Her, They/Them, etc.)"
                            />
                        </div>
                    </o-step-item>
                    <o-step-item icon="search" step="3">
                        <div class="container has-text-centered">
                            <p class="title is-3 has-text-primary">
                                ...and then, we'll add some more details...
                            </p>
                        </div>
                        <div class="p-1">
                            <ValidatedField
                                label="Job Title"
                                :model="model"
                                name="job_title"
                                placeholder="Your job title"
                            />
                            <div class="space-items">
                                <ValidatedField
                                    label="Company"
                                    :model="model"
                                    name="company"
                                    placeholder="Your employer"
                                />
                                <ValidatedField
                                    label="Department"
                                    :model="model"
                                    name="department"
                                    placeholder="Your department"
                                />
                            </div>
                            <ValidatedField
                                label="Work address"
                                :model="model"
                                name="work_address"
                                placeholder="Your work address"
                            />
                            <ValidatedField
                                label="Phone number"
                                :model="model"
                                name="phone_number"
                                placeholder="Your phone number"
                            />
                        </div>
                    </o-step-item>
                    <o-step-item icon="check" step="4">
                        <div class="container has-text-centered">
                            <p class="title is-3 has-text-primary">
                                ...and now, you're all set.
                            </p>
                        </div>
                        <div
                            class="container has-text-centered continue-button"
                        >
                            <o-button
                                icon="check"
                                variant="primary is-large"
                                :disabled="saving"
                                @click="submitUserDetails"
                            >
                                <SpinnerOverlay :active="saving">
                                    <span>Continue to app</span>
                                </SpinnerOverlay>
                            </o-button>
                        </div>
                    </o-step-item>
                    <template #navigation="{ previous, next }">
                        <div
                            class="container has-text-centered nav-buttons p-4"
                        >
                            <o-button
                                outlined
                                variant="link"
                                icon-pack="fas"
                                icon-left="backward"
                                :disabled="previous.disabled"
                                @click.prevent="previous.action"
                            >
                                Previous
                            </o-button>
                            <o-button
                                variant="primary"
                                icon-pack="fas"
                                icon-right="forward"
                                :disabled="next.disabled"
                                @click.prevent="next.action"
                            >
                                Next
                            </o-button>
                        </div>
                    </template>
                </o-steps>
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { Vue, Options } from "vue-class-component";
import ContinueButton from "@/components/ContinueButton.vue";
import ValidatedField from "@/components/ValidatedField.vue";
import { getAxiosInstance } from "@/api/api";
import { Model } from "@/api/model";
import { Contact } from "@/api/contacts";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";

@Options({
    components: {
        ContinueButton,
        ValidatedField,
        SpinnerOverlay,
    },
})
export default class OnboardLayout extends Vue {
    model = new Model(new Contact());
    saving = false;

    submitUserDetails = async () => {
        let instance = getAxiosInstance();
        console.log(instance);
        this.$router.push("/app");
    };
}
</script>

<style scoped>
.column {
    flex-direction: column;
    justify-content: center;
}

.welcome-box {
    width: 40%;
    min-width: 532px;
}

.continue-button {
    margin: 4px 0 0 0;
}

.space-items {
    display: flex;
}

:deep(.space-items > *:not(:last-child)) {
    margin-right: 0.5rem;
}
</style>
