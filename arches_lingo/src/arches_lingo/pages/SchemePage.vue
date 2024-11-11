<script setup lang="ts">
import { ref } from "vue";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import SchemeLicense from "@/arches_lingo/components/scheme/report/SchemeLicense.vue";
import SchemeNote from "@/arches_lingo/components/scheme/report/SchemeNote.vue";
import SchemeUri from "@/arches_lingo/components/scheme/report/SchemeUri.vue";
import SchemeStandard from "@/arches_lingo/components/scheme/report/SchemeStandard.vue";
import SchemeAuthority from "@/arches_lingo/components/scheme/report/SchemeAuthority.vue";
import SchemeEditor from "@/arches_lingo/components/scheme/editor/SchemeEditor.vue";

const editorVisible = ref<boolean>(true);
const sectionVisible = ref<boolean>(true);

const onMaximize = () => {
    editorVisible.value = true;
    sectionVisible.value = false;
};

const onSide = () => {
    editorVisible.value = true;
    editorVisible.value = true;
    sectionVisible.value = true;
};

const onClose = () => {
    editorVisible.value = false;
    sectionVisible.value = true;
};

const onOpenEditor = () => {
    editorVisible.value = true;
    sectionVisible.value = true;
};
</script>

<template>
    <div>
        <Splitter>
            <SplitterPanel
                v-if="sectionVisible"
                size="75"
            >
                <SchemeNote @open-editor="onOpenEditor" />
                <SchemeAuthority @open-editor="onOpenEditor" />
                <SchemeStandard @open-editor="onOpenEditor" />
                <SchemeLicense @open-editor="onOpenEditor" />
                <SchemeUri @open-editor="onOpenEditor" />
            </SplitterPanel>
            <SplitterPanel
                v-if="editorVisible"
                size="25"
            >
                <SchemeEditor
                    :editor-max="sectionVisible"
                    @maximize="onMaximize"
                    @side="onSide"
                    @close="onClose"
                />
            </SplitterPanel>
        </Splitter>
    </div>
</template>
