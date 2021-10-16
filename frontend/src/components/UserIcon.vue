<template>
    <div class="is-relative">
        <transition-group name="fade" mode="out-in">
            <img
                v-show="gravatarLoaded"
                :src="gravatarIconSrc"
                alt=""
                class="img"
                key="gravatar"
                @load="onGravatarLoaded"
                @error="onGravatarLoadError"
            />
            <slot v-if="gravatarLoaded === null" name="loading"></slot>
            <slot v-else-if="gravatarLoaded === false" name="fallback"></slot>
        </transition-group>
    </div>
</template>

<script lang="ts">
import gravatar from "gravatar";
import { defineComponent } from "vue";

export default defineComponent({
    name: "UserIcon",
    props: {
        email: { type: String, default: null },
    },
    data() {
        return { gravatarLoaded: null as boolean | null };
    },
    computed: {
        gravatarIconSrc() {
            if (!this.email) {
                return null;
            }
            return gravatar.url(this.email, { d: "404", s: "200" });
        },
    },
    watch: {
        email(newValue) {
            if (!newValue) {
                console.log("resetting loading state");
                this.gravatarLoaded = null;
            }
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

<style scoped>
.img {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
}
</style>
