<template>
    <div></div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { Contact } from "@/api/contacts";

export default defineComponent({
    name: "BusinessCard",
    props: {
        contact: { type: Object as PropType<Contact>, required: true },
        theme: { type: String, default: null },
    },
});
</script>

<style scoped></style>
