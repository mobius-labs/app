<template>
    <o-field
        :label="label"
        :variant="model.hasErrorsForField(name) ? 'danger' : null"
        :message="model.displayFirstError(name)"
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
import { Model } from "@/api/api";
import { PropType } from "vue";

class Props {
    label!: string;
    name!: string;
    model = prop({
        type: Object as PropType<Model>,
        required: true,
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

    updateValue(v: any) {
        this.model.model[this.name] = v;
    }
}
</script>

<style scoped></style>
