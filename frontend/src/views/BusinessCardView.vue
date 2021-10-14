<template>
    <div
        class="
            has-background-info
            is-flex
            is-flex-direction-column
            is-align-items-center
            is-justify-content-center
        "
        style="height: 100%"
    >
        <BusinessCard
            :contact="{ first_name: 'Chris', job_title: 'Software Developer' }"
        ></BusinessCard>
        <div>
            <h2>Chris is on Mobius</h2>
            <o-button size="large" variant="primary">Join them now</o-button>
        </div>
    </div>
</template>

<script>
import BusinessCard from "@/components/BusinessCard.vue";
export default {
    name: "BusinessCardView",
    components: { BusinessCard },
};
</script>

<style scoped></style>
