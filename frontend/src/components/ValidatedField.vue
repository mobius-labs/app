<template>
    <o-field
        :label="label"
        :variant="hasErrorsForField ? 'danger' : null"
        :message="validationMessage"
    >
        <slot :value="currentValue" :set-value="updateValue">
            <o-input
                :model-value="currentValue"
                :name="name"
                v-bind="$attrs"
                @update:model-value="updateValue"
            />
        </slot>
    </o-field>
</template>

<script lang="ts">
import { prop, Vue } from "vue-class-component";
import { ServerData } from "@/api/api";
import { PropType } from "vue";

class Props {
    label!: string;
    name!: string;
    serverData = prop({
        type: Object as PropType<ServerData>,
        required: true,
    });
    modelValue = prop({
        type: Object as PropType<Record<string, any>>,
        required: true,
    });
}

// This is a wrapper around Oruga's <o-field> component,
// which automatically displays validation error messages we receive from
// the server.
// The hope is that this will make building various forms in the frontend easier.
export default class ValidatedField extends Vue.with(Props) {
    get areErrorsStale() {
        return this.serverData.model[this.name] !== this.modelValue[this.name];
    }

    get currentValue() {
        return this.modelValue[this.name];
    }

    get hasErrorsForField() {
        return !this.areErrorsStale && this.serverData.errors[this.name];
    }

    // if there are errors, show the first one next to the form field.
    // otherwise `null` => no error message
    get validationMessage() {
        if (this.hasErrorsForField) {
            return this.serverData.errors[this.name][0];
        }
        return null;
    }

    updateValue(newValue: any) {
        let newFormValue = {
            ...this.modelValue,
        };
        newFormValue[this.name] = newValue;
        this.$emit("update:modelValue", newFormValue);
    }
}
</script>

<style scoped></style>
