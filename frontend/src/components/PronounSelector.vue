<template>
    <ValidatedField
        v-slot="{ value, setValue }"
        :model="model"
        :update-value="updateValue"
        name="pronouns"
        label="Pronouns"
    >
        <o-select
            ref="pronouns"
            :model-value="value"
            placeholder="Select"
            @update:model-value="setValue"
        >
            <option value=""></option>
            <option value="she/her">she/her</option>
            <option value="he/him">he/him</option>
            <option value="they/them">they/them</option>
        </o-select>
    </ValidatedField>
</template>

<script lang="ts">
import { Vue, Options, prop } from "vue-class-component";
import ValidatedField from "@/components/ValidatedField.vue";
import { PropType } from "vue";
import { Model } from "@/api/model";

class Props {
    model = prop({
        type: Object as PropType<Model>,
        required: true,
    });

    updateValue = prop({
        type: Function as PropType<(x: Record<string, any>) => void | null>,
        default: null,
    });
}

@Options({
    components: {
        ValidatedField,
    },
})
export default class PronounSelector extends Vue.with(Props) {}
</script>

<style scoped></style>
