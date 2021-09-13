<template>
    <o-collapse :open="expanded">
        <template #trigger></template>
        <div
            class="has-background-white-ter p-5 mt-4"
            style="border-radius: 4px"
        >
            <o-field>
                <o-input
                    v-model="code"
                    placeholder="Enter your 6-digit code"
                ></o-input>
            </o-field>
        </div>
    </o-collapse>
</template>

<script lang="ts">
export default {
    name: "VerificationInput",
    props: {
        expanded: {
            type: Boolean,
        },
    },
    data() {
        return {
            code: null,
        };
    },
};
</script>

<style scoped></style>
