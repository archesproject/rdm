<script setup lang="ts">
import { onBeforeUpdate, ref, watch } from "vue";
import { useGettext } from "vue3-gettext";
import Button from "primevue/button";
import SchemeNamespace from "@/arches_lingo/components/scheme/report/SchemeNamespace.vue";
import SchemeStandard from "@/arches_lingo/components/scheme/report/SchemeStandard.vue";
import SchemeLabel from "@/arches_lingo/components/scheme/report/SchemeLabel.vue";
import type { SectionTypes } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();
const EDIT = "edit";
const props = defineProps<{
    editorMax: boolean;
    editorForm: string;
    tileId?: string;
}>();

type SchemeComponent = {
    component: SectionTypes;
    id: string;
    editorName: string;
};

const childRefs = ref<Array<SectionTypes>>([]);
const currentEditor = ref<SchemeComponent>();
const schemeComponents = [
    {
        component: SchemeLabel,
        id: "label",
        editorName: $gettext("Scheme Label"),
    },
    {
        component: SchemeNamespace,
        id: "namespace",
        editorName: $gettext("Scheme Namespace"),
    },
    {
        component: SchemeStandard,
        id: "standard",
        editorName: $gettext("Scheme Standards Followed"),
    },
];

watch(
    props,
    (newValue) => {
        if (newValue) {
            currentEditor.value = schemeComponents.find((component) => {
                return component.id === newValue.editorForm;
            });
        }
    },
    { immediate: true },
);

const emit = defineEmits(["maximize", "side", "close", "updated"]);

onBeforeUpdate(() => {
    childRefs.value = [];
});

function toggleSize() {
    if (props.editorMax) {
        emit("maximize");
    } else {
        emit("side");
    }
}

function onSectionUpdate() {
    emit("updated");
}
</script>

<template>
    <div class="header">
        <div>
            <h3>{{ $gettext("Editor Tools") }}</h3>
            <div>
                <Button
                    :aria-label="$gettext('toggle editor size')"
                    @click="toggleSize"
                >
                    <i
                        :class="{
                            pi: true,
                            'pi-window-maximize': props.editorMax,
                            'pi-window-minimize': !props.editorMax,
                        }"
                        aria-hidden="true"
                    />
                </Button>
                <Button
                    :aria-label="$gettext('close editor')"
                    @click="$emit('close')"
                >
                    <i
                        class="pi pi-times"
                        aria-hidden="true"
                    />
                </Button>
            </div>
        </div>
    </div>
    <div
        v-if="currentEditor"
        class="content"
    >
        <h3>{{ currentEditor.editorName }}</h3>
        <component
            :is="currentEditor.component"
            v-bind="{ mode: EDIT, tileId: tileId }"
            v-on="{ updated: onSectionUpdate }"
        />
    </div>
</template>
<style scoped>
.header div {
    margin: 0 1rem;
    display: flex;
    align-items: center;
}
.header div h3 {
    flex: 1;
}
</style>
