<script setup lang="ts">
import { markRaw, provide, ref } from "vue";

import { useGettext } from "vue3-gettext";

import Button from "primevue/button";

import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import SchemeLabel from "@/arches_lingo/components/scheme/SchemeLabel/SchemeLabel.vue";
import SchemeLicense from "@/arches_lingo/components/scheme/report/SchemeLicense.vue";
import SchemeNote from "@/arches_lingo/components/scheme/report/SchemeNote.vue";
import SchemeNamespace from "@/arches_lingo/components/scheme/report/SchemeNamespace.vue";
import SchemeStandard from "@/arches_lingo/components/scheme/report/SchemeStandard.vue";
import SchemeEditor from "@/arches_lingo/components/scheme/editor/SchemeEditor.vue";
import {
    CLOSED,
    MAXIMIZED,
    MINIMIZED,
    VIEW,
} from "@/arches_lingo/constants.ts";

provide("openEditor", openEditor);
provide("forceSectionRefresh", forceSectionRefresh);

const { $gettext } = useGettext();

const editorPanelKey = ref(0);
const editorTileId = ref();
const editorState = ref(CLOSED);
const selectedComponentDatum = ref();

const componentData = ref([
    {
        component: markRaw(SchemeLabel),
        name: $gettext("Scheme Label"),
        key: 0,
    },
    // { component: SchemeNote, sectionId: "note", props: {}, key: 0 },
    // { component: SchemeStandard, sectionId: "standard", props: {} },
    // { component: SchemeLicense, sectionId: "license", props: {} },
    // { component: SchemeNamespace, sectionId: "namespace", props: {} },
]);

function closeEditor() {
    selectedComponentDatum.value = null;
    editorState.value = CLOSED;
    editorTileId.value = null;
    editorPanelKey.value += 1;
}

function openEditor(componentName: string, tileId?: string) {
    closeEditor();

    selectedComponentDatum.value = componentData.value.find(
        (componentDatum) => {
            return componentDatum.component.componentName === componentName;
        },
    );

    editorTileId.value = tileId;
    editorState.value = MINIMIZED;
}

function maximizeEditor() {
    editorState.value = MAXIMIZED;
}

function minimizeEditor() {
    editorState.value = MINIMIZED;
}

function forceSectionRefresh(componentName: string) {
    const componentDatum = componentData.value.find((componentDatum) => {
        return componentDatum.component.componentName === componentName;
    });

    if (componentDatum) {
        componentDatum.key += 1;
    }
}
</script>

<template>
    <Splitter style="height: 100%">
        <SplitterPanel
            v-show="editorState !== MAXIMIZED"
            :size="66"
        >
            <div
                v-for="component in componentData"
                :key="component.component.componentName + '-' + component.key"
                class="section"
            >
                <div class="header">
                    <h3>{{ component.name }}</h3>
                    <div>
                        <Button
                            label="buttonText"
                            @click="
                                openEditor(component.component.componentName)
                            "
                        ></Button>
                    </div>
                </div>
                <div class="content">
                    <component
                        :is="component.component"
                        :mode="VIEW"
                    />
                </div>
            </div>
        </SplitterPanel>

        <SplitterPanel
            v-if="editorState !== CLOSED"
            :key="editorPanelKey"
            :size="editorState === MINIMIZED ? 33 : 100"
        >
            <SchemeEditor
                :is-editor-maximized="editorState === MAXIMIZED"
                :component="selectedComponentDatum.component"
                :tile-id="editorTileId"
                @maximize="maximizeEditor"
                @minimize="minimizeEditor"
                @close="closeEditor"
            />
        </SplitterPanel>
    </Splitter>
</template>
<style scoped>
.section {
    margin: 0 1rem;
}
.section .header {
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--p-menubar-border-color);
}
.section .header h3 {
    flex: 1;
}
.content {
    margin: 1rem 0;
}
</style>
