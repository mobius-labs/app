<template>
    <div class="bc-wrapper has-text-left">
        <div :class="'bc bc-theme-' + theme">
            <div class="bc-name-title">
                <h2 class="subtitle bc-name">{{ fullName(contact) }}</h2>
                <hr />
                <p class="bc-title">{{ contact.job_title }}</p>
            </div>
            <div class="bc-contact-details"></div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { getFullName, Contact } from "@/api/contacts";

export default defineComponent({
    name: "BusinessCard",
    props: {
        contact: { type: Object as PropType<Contact>, required: true },
        theme: { type: String, default: "default" },
    },
    data() {
        return {
            fullName: getFullName,
        };
    },
});
</script>

<style scoped lang="scss">
.bc-wrapper {
    width: 30rem;
}

.bc-theme-default {
    background-color: white;
    border-radius: 0.5rem;
    padding: 2rem;
}
</style>
