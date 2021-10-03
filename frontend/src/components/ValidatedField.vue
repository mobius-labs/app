<template>
    <o-field
        :label="label"
        :variant="hasErrorsForField ? 'danger' : null"
        :message="validationMessage"
    >
        <slot :value="currentValue" :set-value="updateValue"></slot>
    </o-field>
</template>

<script>
import { Options, Vue } from "vue-class-component";
import { ServerData } from "@/api/api";

// This is a wrapper around Oruga's <o-field> component,
// which automatically displays validation error messages we receive from
// the server.
// The hope is that this will make building various forms in the frontend easier.
@Options({
    props: {
        // a label to display next the field
        label: { type: String, required: true },
        // the `name` of the field should match the attribute name in the API / in Django code
        // i.e.: it probably will be in snake_case
        name: { type: String, required: true },
        // a composite of the previous data sent the server, plus any validation errors
        serverData: { type: ServerData, required: true },
        // the current object containing the form data
        modelValue: { type: Object, required: true },
    },
})
export default class ValidatedField extends Vue {
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

    updateValue(newValue) {
        let newFormValue = {
            ...this.modelValue,
        };
        newFormValue[this.name] = newValue;
        this.$emit("update:modelValue", newFormValue);
    }
}
</script>

<style scoped></style>
