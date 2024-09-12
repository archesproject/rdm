<script setup lang="ts">
import { computed, inject, provide, ref } from "vue";
import { useRouter } from "vue-router";
import { useGettext } from "vue3-gettext";

import Button from "primevue/button";
import ProgressSpinner from "primevue/progressspinner";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";

import { shouldUseContrast } from "@/arches_references/utils.ts";
import {
    CONTRAST,
    SECONDARY,
    displayedRowKey,
    headerKey,
    selectedLanguageKey,
} from "@/arches_lingo/constants.ts";
import { routeNames } from "@/arches_lingo/routes.ts";
import { bestLabel, dataIsConcept } from "@/arches_lingo/utils.ts";
import ConceptTree from "@/arches_lingo/components/tree/ConceptTree.vue";

import type { Ref } from "vue";
import type { Language } from "@/arches/types";
import type { HeaderRefAndSetter, Labellable } from "@/arches_lingo/types";

const { $gettext } = useGettext();
const router = useRouter();
const selectedLanguage = inject(selectedLanguageKey) as Ref<Language>;

const { setHeader } = inject(headerKey) as HeaderRefAndSetter;

const displayedRow: Ref<Labellable | null> = ref(null);
const conceptLabel = computed(() => {
    if (!displayedRow.value) {
        return "Concept detail placeholder";
    }
    return bestLabel(displayedRow.value, selectedLanguage.value.code).value;
});
const setDisplayedRow = (val: Labellable | null) => {
    displayedRow.value = val;
    if (val === null) {
        return;
    }
    if (dataIsConcept(val)) {
        router.push({ name: routeNames.concept, params: { id: val.id } });
        setHeader(conceptLabel.value);
    }
};
// @ts-expect-error vue-tsc doesn't like arbitrary properties here
provide(displayedRowKey, { displayedRow, setDisplayedRow });

const showHierarchy = ref(true);
const toggleHierarchy = () => {
    showHierarchy.value = !showHierarchy.value;
};
</script>

<template>
    <Button
        :severity="shouldUseContrast() ? CONTRAST : SECONDARY"
        :label="$gettext('Toggle hierarchy')"
        @click="toggleHierarchy"
    />
    <Splitter
        style="display: flex; height: 100%"
        :pt="{
            gutter: { style: { display: showHierarchy ? 'flex' : 'none' } },
        }"
    >
        <SplitterPanel
            :size="40"
            :min-size="25"
            :style="{
                display: showHierarchy ? 'flex' : 'none',
                flexDirection: 'column',
            }"
        >
            <Suspense>
                <ConceptTree />
                <template #fallback>
                    <ProgressSpinner />
                </template>
            </Suspense>
        </SplitterPanel>
        <SplitterPanel :min-size="25">
            {{ conceptLabel }}
        </SplitterPanel>
    </Splitter>
</template>
