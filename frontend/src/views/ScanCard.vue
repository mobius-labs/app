<template>
    <div class="is-full-height p-6 page">
        <div style="max-width: 50rem">
            <p>
                <o-button
                    tag="router-link"
                    to="/app/contacts"
                    variant="light"
                    class="mb-4"
                    >Back to contacts...</o-button
                >
            </p>
            <div class="content">
                <h1>Scan Business Card</h1>
                <p>
                    Given an uploaded image, Möbius can automatically create
                    fill-in the details for a contact automatically, using a
                    pre-trained optical character recognition (OCR) model to
                    analyze the uploaded image for key info (name, title,
                    company, website, email, etc...).
                </p>
                <p>
                    Internally, this feature uses the Microsoft
                    <a
                        href="https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/"
                        target="_blank"
                        >Azure Form Recognizer API</a
                    >.
                </p>
                <p class="is-size-7">
                    By using this feature of Möbius you consent to your data
                    being processed by a third-party (Microsoft Azure). For
                    further information, please visit their
                    <a
                        href="https://docs.microsoft.com/en-us/legal/cognitive-services/form-recognizer/fr-data-privacy-security"
                        target="_blank"
                        >Data Privacy & Security</a
                    >
                    page.
                </p>
            </div>

            <div class="is-flex is-flex-direction-column is-align-items-center">
                <o-field label="Input Image">
                    <o-upload v-model="file" drag-drop v-if="!file">
                        <section class="has-text-centered p-6">
                            <p>
                                <o-icon icon="upload" size="is-large"> </o-icon>
                            </p>
                            <p>Drop an image here or click to upload</p>
                        </section>
                    </o-upload>

                    <div
                        v-if="file"
                        class="
                            has-text-centered
                            file-preview
                            has-background-white-ter
                            p-4
                        "
                    >
                        <div>
                            <img :src="objectURL" alt="user selected file" />
                        </div>
                        <div class="mt-3">
                            <em>{{ file.name }}</em>
                            <button
                                v-if="!processing && !result"
                                class="delete ml-3"
                                @click="file = null"
                            ></button>
                        </div>
                    </div>
                </o-field>
            </div>

            <transition name="fade" mode="out-in">
                <div
                    v-if="processing"
                    class="pt-6 pb-6 content has-text-centered"
                >
                    <progress class="progress is-large is-primary"></progress>
                    <em>Analyzing business card</em>
                </div>

                <div v-else-if="result !== null" class="mt-6">
                    <p>Congrats! The image file was analyzed.</p>

                    <div class="buttons mt-3">
                        <o-button
                            tag="router-link"
                            :disabled="!editURL"
                            :to="editURL"
                            icon-left="pencil-alt"
                            variant="primary"
                            >Edit created contact</o-button
                        >
                        <o-button
                            @click="reset"
                            icon-left="redo"
                            variant="light"
                            >Start again</o-button
                        >
                    </div>

                    <o-field label="Process Log" class="mt-3 process-log">
                        <o-input
                            :model-value="logMessages"
                            type="textarea"
                            readonly
                        ></o-input>
                    </o-field>
                </div>

                <div class="buttons is-justify-content-center" v-else>
                    <o-button
                        variant="primary"
                        class="is-medium mt-4 ml-auto mr-auto"
                        v-if="file"
                        @click="submit"
                        >Submit</o-button
                    >
                </div>
            </transition>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { getAxiosInstance } from "@/api/api";
import { defaultToast } from "@/toasts";
import { FullContact } from "@/api/contacts";

interface AnalysisResult {
    item: FullContact;
    messages: string[];
}

export default defineComponent({
    name: "ScanCard",
    data() {
        return {
            file: null as null | File,
            objectURL: null as string | null,
            processing: false,
            result: null as AnalysisResult | null,
        };
    },
    computed: {
        logMessages() {
            const result = (this as any).result;
            if (result) {
                return result.messages.join("\n");
            }
            return "";
        },
        editURL() {
            const result = (this as any).result;
            if (result && result.item && result.item.id) {
                return "/app/contacts/" + result.item.id;
            }
            return "";
        },
    },
    watch: {
        file(f) {
            if (f) {
                this.objectURL = URL.createObjectURL(f);
            } else {
                this.objectURL = null;
            }
        },
    },
    methods: {
        async submit() {
            const formData = new FormData();
            formData.append("image", this.file!);
            this.processing = true;
            try {
                const response = await getAxiosInstance().post(
                    "/contact_book/business_card_ocr",
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    }
                );
                this.result = response.data as AnalysisResult;
            } catch (e) {
                this.$oruga.notification.open(
                    defaultToast(
                        "danger",
                        "There was an error processing the request"
                    )
                );
            }

            this.processing = false;
        },

        reset() {
            this.file = null;
            this.result = null;
        },
    },
});
</script>

<style scoped>
.file-preview {
    max-width: 30rem;
}

.page {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow-y: scroll;
}

/* give this a more "console" look */
.process-log :deep(textarea) {
    font-size: 12px;
}
</style>
