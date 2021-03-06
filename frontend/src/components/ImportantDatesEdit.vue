<template>
    <ContactsOneToMany
        v-slot="{ model, updateItem }"
        ref="oneToMany"
        add-button-text="Add Date"
        title="Important Dates"
        :fresh-item="freshImportantDate"
        api-name="important_date"
        :initial-items="initialItems"
        :server-id="serverId"
        @update:saving="(a, v) => $emit('update:saving', a, v)"
        @update:recently-updated="
            (a, v) => $emit('update:recently-updated', a, v)
        "
    >
        <ValidatedField
            v-slot="{ value, setValue }"
            :label="null"
            :model="model"
            name="important_date_type"
            :update-value="updateItem"
            placeholder="Type"
        >
            <o-dropdown>
                <template #trigger>
                    <o-tooltip
                        label="Click for different date types"
                        position="right"
                    >
                        <o-button size="medium" variant="text">
                            <o-icon
                                v-if="value"
                                :icon="importantDateTypes.get(value)?.icon"
                            ></o-icon>
                            <span v-else>Select type</span>
                        </o-button>
                    </o-tooltip>
                </template>
                <o-dropdown-item
                    v-for="ty in importantDateTypes.values()"
                    :key="ty.label"
                    :value="ty.label"
                    @click="setValue(ty.label)"
                >
                    <o-icon :icon="ty.icon"></o-icon> {{ ty.label }}
                </o-dropdown-item>
                <o-dropdown-item v-if="importantDateTypes.size === 0"
                    >No items</o-dropdown-item
                >
            </o-dropdown>
        </ValidatedField>
        <ValidatedField
            v-slot="{ value, setValue }"
            :model="model"
            name="date"
            :label="null"
            :update-value="updateItem"
            required
        >
            <o-datepicker
                :model-value="value ? new Date(value) : null"
                placeholder="enter date here"
                @update:model-value="(v) => setValue(convertDateToString(v))"
            ></o-datepicker>
        </ValidatedField>
        <o-switch
            :model-value="model.model.get_alert"
            class="mb-4 mt-2"
            @update:model-value="(v) => updateItem({ get_alert: v })"
            >Remind me?</o-switch
        >
    </ContactsOneToMany>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import ContactsOneToMany from "@/components/ContactsOneToMany.vue";
import ValidatedField from "@/components/ValidatedField.vue";
import { getAxiosInstance } from "@/api/api";
import {
    dateToDjangoString,
    ImportantDate,
    ServerContactId,
} from "@/api/contacts";

class Props {
    initialItems!: ImportantDate[];
    serverId!: ServerContactId;
}

interface ImportantDateType {
    label: string;
    icon: string;
}

// A specialized version of ContactsOneToMany, for editing ImportantDates
@Options({
    components: { ContactsOneToMany, ValidatedField },
    emits: ["update:saving", "update:recently-updated"],
})
export default class ImportantDatesEdit extends Vue.with(Props) {
    importantDateTypesSearch = "";
    importantDateTypes = new Map<string, ImportantDateType>();

    get filteredImportantDateTypes() {
        return Array.from(this.importantDateTypes.values());
    }

    async mounted() {
        const response = await getAxiosInstance().get(
            "/contact_book/get_important_date_types/"
        );
        this.importantDateTypes.clear();
        for (const dateType of response.data as ImportantDateType[]) {
            this.importantDateTypes.set(dateType.label, dateType);
        }
    }

    freshImportantDate(): Record<string, any> {
        return { get_alert: true, important_date_type: "Birthday" };
    }

    hasUnsavedChanges() {
        return (
            this.$refs.oneToMany as typeof ContactsOneToMany
        ).hasUnsavedChanges();
    }

    convertDateToString = dateToDjangoString;
}
</script>

<style scoped></style>
