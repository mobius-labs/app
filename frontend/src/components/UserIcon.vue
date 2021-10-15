<template>
    <div
        style="position: relative"
        v-if="!hideOnFailure || gravatarLoaded !== false"
    >
        <transition-group name="fade">
            <img
                v-show="gravatarLoaded"
                :src="gravatarIconSrc"
                alt=""
                style="position: absolute; left: 0; top: 0"
                key="gravatar"
                @load="onGravatarLoaded"
                @error="onGravatarLoadError"
            />
            <slot v-if="!gravatarLoaded" name="fallback"></slot>
        </transition-group>
    </div>
</template>

<script lang="ts">
import gravatar from "gravatar";
import { defineComponent } from "vue";

export default defineComponent({
    name: "UserIcon",
    props: {
        user: { type: Object, default: null },
        hideOnFailure: { type: Boolean, default: false },
    },
    data() {
        return { gravatarLoaded: null as boolean | null };
    },
    emits: ["update:loaded"],
    watch: {
        gravatarLoaded(newVal) {
            this.$emit("update:loaded", newVal);
        },
    },
    computed: {
        gravatarIconSrc() {
            if (this.user == null) {
                return null;
            }
            return gravatar.url(this.user.email, { d: "404", s: "200" });
        },
    },
    methods: {
        onGravatarLoaded() {
            this.gravatarLoaded = true;
        },
        onGravatarLoadError(e: any) {
            console.log(e);
            if (this.gravatarIconSrc !== null) {
                this.gravatarLoaded = false;
            }
        },
    },
});
</script>

<style scoped lang="scss">
@import "../styles/variables";
</style>
