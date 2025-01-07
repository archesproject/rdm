<script setup lang="ts">
import { ref } from "vue";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import SchemeLabel from "@/arches_lingo/components/scheme/report/SchemeLabel.vue";
import SchemeLicense from "@/arches_lingo/components/scheme/report/SchemeLicense.vue";
import SchemeNote from "@/arches_lingo/components/scheme/report/SchemeNote.vue";
import SchemeNamespace from "@/arches_lingo/components/scheme/report/SchemeNamespace.vue";
import SchemeStandard from "@/arches_lingo/components/scheme/report/SchemeStandard.vue";
import SchemeEditor from "@/arches_lingo/components/scheme/editor/SchemeEditor.vue";
import type { SectionTypes } from "@/arches_lingo/types.ts";

const editorVisible = ref(false);
const sectionVisible = ref(true);
const editorForm = ref<string>();
const editorTileId = ref<string>();

const childRefs = ref<Array<SectionTypes>>([]);
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

const onOpenEditor = (form: string, tileId: string) => {
    editorForm.value = form;
    editorVisible.value = true;
    sectionVisible.value = true;
    editorTileId.value = tileId;
};
const onUpdated = () => {
    childRefs.value.forEach((ref) => {
        ref?.getSectionValue();
    });
};

const components = [
    { component: SchemeLabel, id: "label", props: {} },
    { component: SchemeNote, id: "note", props: {} },
    { component: SchemeStandard, id: "standard", props: {} },
    { component: SchemeLicense, id: "license", props: {} },
    { component: SchemeNamespace, id: "namespace", props: {} },
];

const getRef = (el: object | null, index: number) => {
    if (el != null) childRefs.value[index] = el as SectionTypes;
};
</script>

<template>
    <Splitter style="height: 100%">
        <SplitterPanel
            v-if="sectionVisible"
            :size="66"
            :min-size="33"
        >
            <template
                v-for="(component, index) in components"
                :key="component.id"
            >
                <component
                    :is="component.component"
                    :ref="(el) => getRef(el, index)"
                    v-bind="component.props"
                    @open-editor="
                        (tileId: string) => {
                            onOpenEditor(component.id, tileId);
                        }
                    "
                />
            </template>
        </SplitterPanel>
        <SplitterPanel
            v-if="editorVisible"
            :size="33"
            :min-size="33"
        >
            <SchemeEditor
                v-if="editorForm"
                :editor-max="sectionVisible"
                :editor-form="editorForm"
                :tile-id="editorTileId"
                @maximize="onMaximize"
                @side="onSide"
                @close="onClose"
                @updated="onUpdated"
            />
        </SplitterPanel>
    </Splitter>
</template>
