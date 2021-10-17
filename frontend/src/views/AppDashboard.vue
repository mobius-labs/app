<template>
    <div style="overflow-y: scroll; height: 100%">
        <div class="hero is-primary is-medium">
            <div class="hero-body">
                <h1 v-if="firstName" class="title is-1 fade-in-text">
                    Hello, {{ firstName }}.
                </h1>
                <h2 class="subtitle is-size-4 mt-2 fade-in-text">
                    Here's what's coming up in the next
                    <InlineSelect
                        :model-value="timeframe"
                        @update:model-value="(v) => (timeframe = v)"
                        :options="timeframeOptions"
                    ></InlineSelect>
                </h2>
            </div>
        </div>
        <div>
            <o-collapse
                class="card"
                animation="slide"
                v-for="(collapse, index) of collapses"
                :key="index"
                :open="true"
                @open="isOpen = index"
            >
                <template #trigger="props">
                    <div class="card-header has-background-white" role="button">
                        <p class="card-header-title">
                            <span
                                v-if="
                                    collapse.mode === 'catchUps' &&
                                    collapse.overdue
                                "
                            >
                                <span>Overdue Catch-ups</span>
                                <span
                                    :class="
                                        'tag ml-3 is-rounded is-light ' +
                                        (overdueCatchups.length
                                            ? 'is-danger'
                                            : 'is-primary')
                                    "
                                    >{{ overdueCatchups.length }}</span
                                >
                            </span>
                            <span
                                v-else-if="
                                    collapse.mode === 'catchUps' &&
                                    !collapse.overdue
                                "
                            >
                                <span>Upcoming Catch-Ups</span>
                                <span
                                    class="
                                        tag
                                        ml-3
                                        is-rounded is-primary is-light
                                    "
                                    v-if="futureCatchups"
                                    >{{ futureCatchups.length }}</span
                                >
                            </span>
                            <span v-else>
                                <span>Important Dates</span>
                                <span
                                    class="
                                        tag
                                        ml-3
                                        is-rounded is-primary is-light
                                    "
                                    v-if="importantDates.results"
                                    >{{ importantDates.results.length }}</span
                                >
                            </span>
                        </p>
                        <a class="card-header-icon">
                            <o-icon
                                :icon="props.open ? 'caret-up' : 'caret-down'"
                            >
                            </o-icon>
                        </a>
                    </div>
                </template>
                <div
                    class="card-content is-relative"
                    style="min-height: 6rem"
                    v-if="collapse.mode === 'catchUps'"
                >
                    <div v-if="catchUps.results">
                        <div
                            v-for="catchUp in collapse.overdue
                                ? overdueCatchups
                                : futureCatchups"
                            :key="catchUp.contact.id"
                            :class="
                                'catchup level notification ' +
                                (collapse.overdue && !catchUp.stale
                                    ? 'overdue is-danger is-light'
                                    : 'not-overdue')
                            "
                        >
                            <div class="level-left">
                                <div>
                                    <p class="mb-3">
                                        <span class="subtitle has-text-black">{{
                                            fullName(catchUp.contact)
                                        }}</span>
                                    </p>
                                    <p v-if="collapse.overdue">
                                        {{ catchUp.contact.first_name }} is
                                        <strong
                                            >{{
                                                displayDateDelta(
                                                    catchUp.catchUpDate
                                                )
                                            }}
                                            days overdue</strong
                                        >
                                        for a catch up.
                                    </p>
                                    <p v-if="collapse.overdue">
                                        You last caught up with
                                        {{ catchUp.contact.first_name }} on
                                        {{
                                            displayDateStr(
                                                catchUp.contact
                                                    .last_time_contacted
                                            )
                                        }}
                                    </p>
                                    <p v-else>
                                        You are due to catch up with
                                        {{ catchUp.contact.first_name }} by
                                        {{ displayDate(catchUp.catchUpDate) }}
                                    </p>
                                </div>
                            </div>
                            <div class="level-right">
                                <div>
                                    <o-button
                                        v-if="collapse.overdue"
                                        :disabled="catchUp.stale"
                                        @click="markCaughtUp(catchUp)"
                                        >We've caught up since!</o-button
                                    >
                                    <p>
                                        <o-button
                                            tag="router-link"
                                            variant="text"
                                            :to="
                                                '/app/contacts/' +
                                                catchUp.contact.id
                                            "
                                            class="ml-3 mt-3"
                                            icon-left="pencil-alt"
                                            >Edit
                                            {{ catchUp.contact.first_name }}'s
                                            details</o-button
                                        >
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div
                            v-if="
                                (collapse.overdue
                                    ? overdueCatchups
                                    : futureCatchups
                                ).length === 0
                            "
                        >
                            <h2 class="subtitle m-4 has-text-centered">
                                <em>You're all clear!</em>
                            </h2>
                        </div>
                    </div>
                    <o-loading
                        :active="!catchUps.results"
                        :full-page="false"
                    ></o-loading>
                </div>
                <div
                    class="card-content is-relative"
                    v-else-if="collapse.mode === 'importantDates'"
                >
                    <div v-if="importantDates.results">
                        <div
                            v-for="impDate in importantDates.results"
                            :key="impDate.id"
                            class="
                                notification
                                level
                                catchup
                                important-date
                                is-warning is-light
                            "
                        >
                            <div class="level-left">
                                <div>
                                    <h2
                                        class="subtitle"
                                        v-if="
                                            impDate.important_date_type ===
                                            'Birthday'
                                        "
                                    >
                                        <o-icon icon="birthday-cake"></o-icon>
                                        It's
                                        <strong
                                            >{{ fullName(impDate.contact) }}'s
                                            birthday</strong
                                        >
                                        on {{ displayDateStr(impDate.date) }}
                                    </h2>
                                    <h2
                                        class="subtitle"
                                        v-else-if="
                                            impDate.important_date_type ===
                                            'Anniversary'
                                        "
                                    >
                                        <o-icon icon="ring"></o-icon>
                                        <strong>{{
                                            fullName(impDate.contact)
                                        }}</strong>
                                        has their
                                        <strong>anniversary</strong> on
                                        {{ displayDateStr(impDate.date) }}
                                    </h2>
                                    <h2 class="subtitle" v-else>
                                        <o-icon icon="calendar-day"></o-icon>
                                        {{ displayDateStr(impDate.date) }} is an
                                        important date for
                                        <strong>{{
                                            fullName(impDate.contact)
                                        }}</strong>
                                    </h2>

                                    <p
                                        v-if="
                                            impDate.important_date_type ===
                                            'Birthday'
                                        "
                                    >
                                        Don't forget to wish them a happy
                                        birthday!
                                    </p>
                                    <p
                                        v-else-if="
                                            impDate.important_date_type ===
                                            'Anniversary'
                                        "
                                    >
                                        Don't forget to wish them a happy
                                        anniversary!
                                    </p>
                                </div>
                            </div>

                            <div class="level-right has-text-black">
                                <div>
                                    <o-switch
                                        :model-value="impDate.get_alert"
                                        @update:model-value="
                                            (v) => updateDateAlert(impDate, v)
                                        "
                                    >
                                        <span v-if="impDate.get_alert"
                                            >Receive notifications</span
                                        >
                                        <span v-else
                                            >Don't receive notifications</span
                                        >
                                    </o-switch>
                                    <p>
                                        <o-button
                                            tag="router-link"
                                            variant="text"
                                            :to="
                                                '/app/contacts/' +
                                                impDate.contact.id
                                            "
                                            class="ml-3 mt-3"
                                            icon-left="pencil-alt"
                                            >Edit
                                            {{ impDate.contact.first_name }}'s
                                            details</o-button
                                        >
                                    </p>
                                </div>
                            </div>
                            <!--                             <o-button tag="router-link" :to="'/app/contacts/' + impDate.contact.id" variant="light" icon-left="user-edit" style="padding-top: 0"></o-button>-->
                            <!--                                 {{ impDate }}-->

                            <!--                             <h2 class="subtitle">{{ fullName(catchUp.contact) }} <o-button tag="router-link" :to="'/app/contacts/' + catchUp.contact.id" variant="light" icon-left="user-edit" style="padding-top: 0"></o-button></h2>-->
                            <!--                             <p v-if="collapse.overdue">{{ catchUp.contact.first_name }} is <span class="has-text-danger">{{ displayDateDelta(catchUp.catchUpDate) }} days overdue</span> for a catch up.</p>-->
                            <!--                             <p v-if="collapse.overdue">You last caught up with {{ catchUp.contact.first_name }} on {{ displayDateStr(catchUp.contact.last_time_contacted) }}</p>-->
                            <!--                             <p v-else>You are due to catch up with {{ catchUp.contact.first_name }} by {{ displayDate(catchUp.catchUpDate) }}</p>-->
                        </div>
                        <div v-if="importantDates.length === 0">
                            <h2 class="subtitle m-6 has-text-centered">
                                <em>Nothing coming up!</em>
                            </h2>
                        </div>
                    </div>
                    <o-loading
                        :active="!importantDates.results"
                        :full-page="false"
                    ></o-loading>
                </div>
            </o-collapse>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { getAxiosInstance, ListResponse } from "@/api/api";
import {
    dateToDjangoString,
    FullContact,
    getFullName,
    ImportantDateContact,
} from "@/api/contacts";
import { DateTime, Duration, Interval } from "luxon";
import { defaultToast } from "@/toasts";
import InlineSelect from "@/components/InlineSelect.vue";

const DEFAULT_TIMEFRAME = "7";

class ContactCatchUp {
    contact: FullContact;
    catchUpDate: DateTime;
    stale: boolean;

    constructor(contact: FullContact) {
        this.contact = contact;
        this.stale = false;
        this.catchUpDate = DateTime.fromISO(
            this.contact.last_time_contacted || ""
        ).plus(
            Duration.fromObject({
                days: 365 / this.contact.regularity_of_contact!,
            })
        );
    }
}

export default defineComponent({
    name: "AppDashboard",
    components: { InlineSelect },
    data() {
        return {
            userContact: null as FullContact | null,
            isOpen: 1,
            collapses: [
                {
                    mode: "catchUps",
                    overdue: true,
                },
                {
                    mode: "catchUps",
                    overdue: false,
                },
                {
                    mode: "importantDates",
                },
            ],
            timeframeOptions: {
                "1": "day",
                "7": "week",
                "14": "fortnight",
                "30": "month",
            },
            catchUps: {
                count: 0,
                next: null as string | null,
                previous: null as string | null,
                results: null as ContactCatchUp[] | null,
            },
            importantDates: {
                count: 0,
                next: null as string | null,
                previous: null as string | null,
                results: null as ImportantDateContact[] | null,
            },
            timeframe: DEFAULT_TIMEFRAME,
        };
    },
    watch: {
        timeframe() {
            this.fetchCatchUps();
            this.fetchImportantDates();
        },
    },
    computed: {
        firstName(): string | null {
            return this.userContact?.first_name || null;
        },
        overdueCatchups(): ContactCatchUp[] {
            return (
                this.catchUps.results?.filter((c) =>
                    this.isOverdue(c.catchUpDate)
                ) || []
            );
        },
        futureCatchups(): ContactCatchUp[] {
            return (
                this.catchUps.results?.filter(
                    (c) => !this.isOverdue(c.catchUpDate)
                ) || []
            );
        },
    },
    mounted() {
        this.fetchCatchUps();
        this.fetchUserFirstName();
        this.fetchImportantDates();
    },
    methods: {
        async fetchCatchUps() {
            this.catchUps.results = null;
            const response = await getAxiosInstance().get(
                "/contact_book/catchup_countdown/" + this.timeframe
            );
            const data = response.data as ListResponse<FullContact>;
            this.catchUps = {
                ...data,
                results: data.results
                    .map((c) => new ContactCatchUp(c))
                    .sort((c1, c2) => {
                        return (
                            c1.catchUpDate.toMillis() -
                            c2.catchUpDate.toMillis()
                        );
                    }),
            };
        },
        async fetchImportantDates() {
            const response = await getAxiosInstance().get(
                "/contact_book/imp_date_countdown/" + this.timeframe
            );
            console.log(response.data);
            const data = response.data as ListResponse<ImportantDateContact>;
            this.importantDates = {
                ...data,
                results: data.results.sort((i1, i2) => {
                    return (
                        DateTime.fromISO(i1.date).toMillis() -
                        DateTime.fromISO(i2.date).toMillis()
                    );
                }),
            };
        },
        async fetchUserFirstName() {
            const response = await getAxiosInstance().get(
                "/contact_book/get_user_contacts"
            );
            this.userContact = response.data as FullContact;
        },
        fullName: getFullName,
        isOverdue(date: DateTime) {
            return date < DateTime.now();
        },
        displayDateDelta(date: DateTime) {
            const now = DateTime.now();
            const duration = Interval.fromDateTimes(
                now > date ? date : now,
                now > date ? now : date
            ).toDuration();
            console.log(duration);
            return Math.round(duration.as("days"));
        },
        displayDate(date: DateTime) {
            return date.toLocaleString(DateTime.DATE_FULL);
        },
        displayDateStr(date: string) {
            return this.displayDate(DateTime.fromISO(date));
        },
        async markCaughtUp(catchUp: ContactCatchUp) {
            try {
                catchUp.contact.last_time_contacted = dateToDjangoString(
                    DateTime.now().toJSDate()
                );
                catchUp.stale = true;
                await getAxiosInstance().put(
                    "/contact_book/update_contact_by_id/" + catchUp.contact.id,
                    catchUp.contact
                );
                setTimeout(() => {
                    this.fetchCatchUps();
                }, 2000);
                this.$oruga.notification.open(
                    defaultToast(
                        "success",
                        "Your catch up with " +
                            catchUp.contact.first_name +
                            " has been recorded."
                    )
                );
            } catch (e) {
                this.$oruga.notification.open(
                    defaultToast(
                        "warning",
                        "Oops! Failed to modify this contact."
                    )
                );
            }
        },
        async updateDateAlert(impDate: ImportantDateContact, value: boolean) {
            try {
                impDate.get_alert = value;
                await getAxiosInstance().put(
                    "/contact_book/update_important_date_by_iid/" + impDate.id,
                    impDate
                );
                this.$oruga.notification.open(
                    defaultToast(
                        "success",
                        "You will" +
                            (!value ? "  no longer" : "") +
                            " be alerted about this important date"
                    )
                );
            } catch (e) {
                this.$oruga.notification.open(
                    defaultToast(
                        "warning",
                        "Oops! Failed to modify this important date."
                    )
                );
            }
        },
    },
});
</script>

<style scoped lang="scss">
@import "../styles/variables.scss";

.fade-in-text {
    animation: fadeIn 2s;
}

@keyframes fadeIn {
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
}

.catchup {
    transition: background 0.5s ease;
}

.catchup.overdue {
    background: linear-gradient(90deg, lighten(#b60000, 60%), $white);

    &:hover {
        box-shadow: 0 0 4px lighten(#b60000, 50%);
    }
}

.catchup.not-overdue {
    background: linear-gradient(90deg, $grey-lighter, $white);

    &:hover {
        box-shadow: 0 0 4px darken($grey-lighter, 5%);
    }
}

.catchup.important-date {
    background: linear-gradient(90deg, lighten($warning, 15%), $white);

    &:hover {
        box-shadow: 0 0 4px lighten($warning, 10%);
    }
}
</style>
