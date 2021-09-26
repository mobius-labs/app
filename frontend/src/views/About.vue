<template>
    <div class="about">
        <h1>This is an about page</h1>
        <p class="some-class">
            This is some about content! And some more content!
        </p>
        <o-button :disabled="amount <= 0" @click="amount--">Subtract</o-button>
        <o-button @click="amount++">Add</o-button>
        <p>The amount is {{ amount }}</p>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
    setup() {
        const amount = ref(0);
        return { amount };
    },
});
</script>

<style scoped lang="scss">
.some-class {
    color: red;
}
</style>
