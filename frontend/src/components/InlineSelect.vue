<template>
    <o-dropdown class="has-background-primary">
        <template #trigger="{ active }">
            <span class="trigger">
                <span class="underlined">{{ display }}</span>
                <transition name="fade" mode="out-in">
                    <o-icon icon="caret-up" v-if="active" class="ml-1"></o-icon>
                    <o-icon icon="caret-down" v-else class="ml-1"></o-icon>
                </transition>
            </span>
        </template>
        <o-dropdown-item
            v-for="display in notCurrentlySelectedOptions"
            :key="display[0]"
            @click="$emit('update:model-value', display[0])"
        >
            <span class="subtitle">{{ display[1] }}</span>
        </o-dropdown-item>
    </o-dropdown>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "InlineSelect",
    props: {
        options: { type: Object, required: true },
        modelValue: { type: String, required: true },
    },
    computed: {
        display() {
            return this.options[this.modelValue];
        },
        notCurrentlySelectedOptions() {
            return Object.entries(this.options).filter((value) => {
                return value[0] !== this.modelValue;
            });
        },
    },
});
</script>

<style scoped lang="scss">
@import "../styles/variables.scss";

.trigger {
    padding: 0.5rem 0.5rem 1rem 0.2rem;
    border-radius: 10px;
    color: #eee;
    transition: background-color 1s ease;

    &:hover {
        color: #fff;
        cursor: pointer;
        //background-color: rgba(255, 255, 255, 0.05);
    }
}

.underlined {
    position: relative;
}

.underlined:before {
    content: "";
    position: absolute;
    width: 100%;
    height: 2px;
    bottom: -3px;
    left: 0;
    background-color: #fff;
    visibility: hidden;
    transform: scaleX(0);
    transition: all 0.3s ease-in-out;
}

.trigger:hover .underlined:before {
    visibility: visible;
    transform: scaleX(1);
}

:deep(.dropdown-content) {
    background-color: $primary;
}

:deep(.dropdown-item.is-active) {
    background-color: transparent;
}

:deep(.dropdown-item:hover) {
    background-color: rgba(255, 255, 255, 0.2);
}
</style>
