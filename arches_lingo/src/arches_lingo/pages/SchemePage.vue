<script setup lang="ts">
import { computed, markRaw, provide, ref } from "vue";

import { useGettext } from "vue3-gettext";
import { useRoute } from "vue-router";

import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import SchemeLabel from "@/arches_lingo/components/scheme/SchemeLabel/SchemeLabel.vue";
import SchemeLicense from "@/arches_lingo/components/scheme/report/SchemeLicense.vue";
import SchemeNote from "@/arches_lingo/components/scheme/report/SchemeNote.vue";
import SchemeNamespace from "@/arches_lingo/components/scheme/report/SchemeNamespace.vue";
import SchemeStandard from "@/arches_lingo/components/scheme/SchemeStandard/SchemeStandard.vue";
import SchemeEditor from "@/arches_lingo/components/scheme/editor/SchemeEditor.vue";
import {
    CLOSED,
    MAXIMIZED,
    MINIMIZED,
    NEW,
    VIEW,
} from "@/arches_lingo/constants.ts";

provide("openEditor", openEditor);
provide("forceSectionRefresh", forceSectionRefresh);

const route = useRoute();
const { $gettext } = useGettext();

const editorPanelKey = ref(0);
const editorTileId = ref();
const editorState = ref(CLOSED);
const selectedComponentDatum = ref();

const resourceInstanceId = computed<string | undefined>(() => {
    if (route.params.id !== NEW) {
        return route.params.id as string;
    }

    return undefined;
});

const componentData = ref([
    {
        component: markRaw(SchemeLabel),
        componentName: "SchemeLabel",
        name: $gettext("Scheme Label"),
        graphSlug: "scheme",
        nodeGroupAlias: "appellative_status",
        key: 0,
    },
    {
        component: markRaw(SchemeStandard),
        componentName: "SchemeStandard",
        name: $gettext("Scheme Standard"),
        graphSlug: "scheme",
        nodeGroupAlias: "creation",
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
            return componentDatum.componentName === componentName;
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
        return componentDatum.componentName === componentName;
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
            <component
                :is="componentDatum.component"
                v-for="componentDatum in componentData"
                :key="componentDatum.componentName + '-' + componentDatum.key"
                :graph-slug="componentDatum.graphSlug"
                :node-group-alias="componentDatum.nodeGroupAlias"
                :resource-instance-id="resourceInstanceId"
                :mode="VIEW"
            />
        </SplitterPanel>

        <SplitterPanel
            v-if="editorState !== CLOSED"
            :key="editorPanelKey"
            :size="editorState === MINIMIZED ? 33 : 100"
        >
            <SchemeEditor
                :is-editor-maximized="editorState === MAXIMIZED"
                :component="selectedComponentDatum.component"
                :component-name="selectedComponentDatum.componentName"
                :graph-slug="selectedComponentDatum.graphSlug"
                :node-group-alias="selectedComponentDatum.nodeGroupAlias"
                :resource-instance-id="resourceInstanceId"
                :tile-id="editorTileId"
                @maximize="maximizeEditor"
                @minimize="minimizeEditor"
                @close="closeEditor"
            />
        </SplitterPanel>
    </Splitter>
</template>
