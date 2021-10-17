<template>
    <section class="hero is-primary is-fullheight">
        <div class="hero-body column">
            <div class="box is-white has-content-centered welcome-box">
                <o-steps
                    v-model="activeStep"
                    animated
                    rounded
                    custom-navigation
                >
                    <o-step-item icon="birthday-cake" step="0">
                        <div class="container has-text-centered">
                            <p class="title is-2 has-text-primary">
                                Congratulations on creating your account!
                            </p>
                            <p class="title is-4 has-text-primary">
                                Now, let's get to know you.
                            </p>
                        </div>
                    </o-step-item>
                    <o-step-item icon="user" step="1">
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
                            <PronounSelector :model="model" />
                        </div>
                    </o-step-item>
                    <o-step-item icon="search" step="2">
                        <div class="container has-text-left">
                            <p class="title is-3 has-text-primary mb-2">
                                And then, we'll add some more details...
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
                    <o-step-item icon="check" step="3">
                        <div class="container has-text-centered">
                            <p class="title is-3 has-text-primary">
                                ...and now, you're all set.
                            </p>
                        </div>
                        <div class="container has-text-centered mt-5">
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
                                variant="primary mr-2"
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
import ValidatedField from "@/components/ValidatedField.vue";
import { getAxiosInstance } from "@/api/api";
import { Model } from "@/api/model";
import { Contact } from "@/api/contacts";
import SpinnerOverlay from "@/components/SpinnerOverlay.vue";
import { defaultToast } from "@/toasts";
import PronounSelector from "@/components/PronounSelector.vue";

@Options({
    components: {
        PronounSelector,
        ValidatedField,
        SpinnerOverlay,
    },
    watch: {
        activeStep: "printActiveStep",
    },
})
export default class OnboardLayout extends Vue {
    model = new Model(new Contact());
    saving = false;
    activeStep = 1;

    async submitUserDetails() {
        await this.model.tryUpdate(
            async () => {
                const response = await getAxiosInstance().request({
                    url: "contact_book/create_user_contact",
                    method: "POST",
                    data: this.model.model,
                });

                if (response.status === 201) {
                    console.log("good request!");
                    this.$oruga.notification.open(
                        defaultToast("info", "Contact created")
                    );
                    this.model.captureServerResponse(response.data as Contact);
                    await this.$router.push("/app");
                }
            },
            undefined,
            this.onError.bind(this)
        );
    }

    printActiveStep() {
        console.log(this.activeStep);
    }

    onError() {
        if (
            this.model.hasErrorsForFields([
                "title",
                "first_name",
                "middle_name",
                "surname",
                "pronouns",
            ])
        ) {
            this.activeStep = 2;
        } else if (
            this.model.hasErrorsForFields([
                "job_title",
                "company",
                "department",
            ])
        ) {
            this.activeStep = 3;
        } else {
            this.activeStep = 1;
        }
    }
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

.space-items {
    display: flex;
}

:deep(.space-items > *:not(:last-child)) {
    margin-right: 0.5rem;
}
</style>
