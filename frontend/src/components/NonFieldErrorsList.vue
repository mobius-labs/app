<template>
    <div class="content">
        <div
            v-for="(error, i) in nonFieldErrors"
            :key="i"
            class="notification is-info has-text-centered"
        >
            {{ error }}
        </div>
    </div>
</template>

<script lang="ts">
import { prop, Vue } from "vue-class-component";
import { PropType } from "vue";
import { Model } from "@/api/api";

class Props {
    model = prop({
        type: Object as PropType<Model>,
        required: true,
    });
}

export default class NonFieldErrorsList extends Vue.with(Props) {
    get nonFieldErrors() {
        if (!this.model.matchesServer()) {
            return [];
        } else {
            return this.model.nonFieldErrors;
        }
    }
}
</script>

<style scoped></style>
