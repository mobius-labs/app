<template>
    <div :class="'input' + (expanded ? ' expanded' : '')">
        <transition mode="in-out">
            <div class="content">
                <o-field>
                    <o-input
                        v-model="code"
                        placeholder="Enter your 6-digit code"
                    ></o-input>
                </o-field>
                <p class="resend">
                    <a href="">Resend code</a>
                </p>
            </div>
        </transition>
    </div>
</template>

<script lang="ts">
export default {
    name: "VerificationInput",
    props: {
        expanded: {
            Type: Boolean,
        },
    },
    data() {
        return {
            code: null,
        };
    },
};
</script>

<style scoped>
.content {
    display: flex;
    flex-direction: column;
}

.input {
    overflow: auto;
    height: 0;
    flex: 0;
    padding: 0 0;
    transition: height 2s ease, flex 2s ease;
    border: transparent;
}
.expanded {
    flex: 1;
    min-height: 6rem;
    margin: 1rem 0rem;
}

.resend {
    text-align: left;
}
</style>
