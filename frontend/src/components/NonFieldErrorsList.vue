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

<script>
import { Options, Vue } from "vue-class-component";

@Options({
    props: { nonFieldErrors: Array, default: [] },
})
export default class NonFieldErrorsList extends Vue {}
</script>

<style scoped></style>
