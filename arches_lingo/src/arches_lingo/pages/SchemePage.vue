<script setup lang="ts">
import { markRaw, provide, ref } from "vue";

import { useGettext } from "vue3-gettext";

import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import SchemeLabel from "@/arches_lingo/components/scheme/SchemeLabel/SchemeLabel.vue";
import SchemeLicense from "@/arches_lingo/components/scheme/report/SchemeLicense.vue";
import SchemeNote from "@/arches_lingo/components/scheme/report/SchemeNote.vue";
import SchemeNamespace from "@/arches_lingo/components/scheme/report/SchemeNamespace.vue";
import SchemeStandard from "@/arches_lingo/components/scheme/report/SchemeStandard.vue";
import SchemeEditor from "@/arches_lingo/components/scheme/editor/SchemeEditor.vue";
import { VIEW } from "@/arches_lingo/constants.ts";

const { $gettext } = useGettext();

provide("openEditor", openEditor);
provide("forceSectionRefresh", forceSectionRefresh);

const editorPanelKey = ref(0);
const editorVisible = ref(false);
const sectionVisible = ref(true);
const editorTileId = ref<string>();

const onMaximize = () => {
    editorVisible.value = true;
    sectionVisible.value = false;
};

const onMinimize = () => {
    editorVisible.value = true;
    sectionVisible.value = true;
};

const onClose = () => {
    editorVisible.value = false;
    sectionVisible.value = true;
};

// Make the components array reactive and include a key for SchemeLabel
const components = ref([
    {
        component: markRaw(SchemeLabel),
        name: $gettext("Scheme Label"),
        id: "label",
        key: 0,
    },
    // { component: SchemeNote, id: "note", props: {}, key: 0 },
    // { component: SchemeStandard, id: "standard", props: {} },
    // { component: SchemeLicense, id: "license", props: {} },
    // { component: SchemeNamespace, id: "namespace", props: {} },
]);

function closeEditor() {
    editorVisible.value = false;
    sectionVisible.value = true;
    editorTileId.value = undefined;

    editorPanelKey.value++;
}

function openEditor(tileId?: string) {
    closeEditor();

    editorVisible.value = true;
    sectionVisible.value = true;
    editorTileId.value = tileId;
}

function forceSectionRefresh() {
    const labelComponent = components.value.find((c) => c.id === "label");
    if (labelComponent) {
        labelComponent.key++;
    }
}
</script>

<template>
    <Splitter style="height: 100%">
        <SplitterPanel
            v-if="sectionVisible"
            :size="66"
            :min-size="33"
        >
            <template
                v-for="component in components"
                :key="component.id + '-' + component.key"
            >
                <component
                    :is="component.component"
                    :mode="VIEW"
                />
            </template>
        </SplitterPanel>
        <SplitterPanel
            v-if="editorVisible"
            :key="editorPanelKey"
            :size="33"
            :min-size="33"
        >
            <SchemeEditor
                :editor-max="sectionVisible"
                :component="{ component: SchemeLabel, id: 'label' }"
                :tile-id="editorTileId"
                @maximize="onMaximize"
                @minimize="onMinimize"
                @close="onClose"
            />
        </SplitterPanel>
    </Splitter>
</template>
