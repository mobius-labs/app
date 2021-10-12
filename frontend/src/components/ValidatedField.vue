<template>
    <o-field
        :label="derivedLabel"
        :variant="
            model.hasErrorsForField(name) || model.nonFieldErrors.length > 0
                ? 'danger'
                : null
        "
        :message="model.displayFirstError(name)"
    >
        <slot :value="currentValue" :set-value="doUpdateValue">
            <o-input
                :model-value="currentValue"
                :name="name"
                v-bind="$attrs"
                @update:model-value="doUpdateValue"
            />
        </slot>
    </o-field>
</template>

<script lang="ts">
import { prop, Vue } from "vue-class-component";
import { Model } from "@/api/api";
import { PropType } from "vue";
import { convertToTitleCase } from "@/api/utils";

class Props {
    label?: string | null;
    name!: string;
    model = prop({
        type: Object as PropType<Model>,
        required: true,
    });
    updateValue = prop({
        // eslint-disable-next-line no-unused-vars
        type: Function as PropType<(x: Record<string, any>) => void | null>,
        default: null,
    });
}

// This is a wrapper around Oruga's <o-field> component,
// which automatically displays validation error messages we receive from
// the server.
// The hope is that this will make building various forms in the frontend easier.
export default class ValidatedField extends Vue.with(Props) {
    get currentValue() {
        return this.model.model[this.name];
    }

    get derivedLabel() {
        if (this.label === "none") {
            return null;
        }
        if (typeof this.label === "undefined") {
            return convertToTitleCase(this.name.replace("_", " "));
        }
        return this.label;
    }

    doUpdateValue(v: any) {
        if (this.updateValue !== null) {
            let update: Record<string, any> = {};
            update[this.name] = v;
            this.updateValue(update);
            return;
        }
        this.model.model[this.name] = v;
    }
}
</script>

<style scoped></style>
