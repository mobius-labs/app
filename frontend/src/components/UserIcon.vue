<template>
    <img
        v-if="showGravatar"
        :src="gravatarIconSrc"
        alt=""
        class="gravatar-image"
    />
    <o-button variant="info" v-else-if="fallback">
        <o-icon icon="user" size="medium" variant="primary" />
    </o-button>
</template>

<script lang="ts">
import gravatar from "gravatar";
import { defineComponent } from "vue";

export default defineComponent({
    name: "UserIcon",
    props: {
        user: { type: Object, default: null },
        fallback: { type: Boolean, default: true },
    },
    data() {
        return { showGravatar: false };
    },
    watch: { user: "onUserUpdated" },
    computed: {
        gravatarIconSrc() {
            if (this.user == null) {
                return null;
            }
            return gravatar.url(this.user.email, { d: "404" });
        },
    },
    methods: {
        async onUserUpdated() {
            let showGravatar = true;
            try {
                const result = await window.fetch(
                    this.gravatarIconSrc as string
                );
                if (!result.ok) {
                    showGravatar = false;
                }
            } catch (e) {
                console.log("disabling gravatar");
                showGravatar = false;
            }
            this.showGravatar = showGravatar;
        },
    },
});
</script>

<style scoped lang="scss">
@import "../styles/variables";
</style>
