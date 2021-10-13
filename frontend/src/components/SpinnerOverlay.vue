<template>
    <div>
        <div class="icon-container">
            <Spinner v-if="active" />
        </div>
        <div :class="active ? 'hide-text' : ''">
            <slot />
        </div>
    </div>
</template>

<script>
import { Options, Vue } from "vue-class-component";
import Spinner from "@/components/Spinner";

@Options({
    props: {
        active: {
            type: Boolean,
            default: true,
        },
    },
    components: { Spinner },
})
export default class SpinnerOverlay extends Vue {}
</script>

<style scoped>
.icon-container {
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

.hide-text {
    visibility: hidden;
}
</style>
