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
import {
    bestLabel,
    dataIsConcept,
    dataIsScheme,
} from "@/arches_lingo/utils.ts";
import ConceptDetail from "@/arches_lingo/components/detail/ConceptDetail.vue";
import ConceptTree from "@/arches_lingo/components/tree/ConceptTree.vue";
import SchemeDetail from "@/arches_lingo/components/detail/SchemeDetail.vue";

import type { Ref } from "vue";
import type { Language } from "@/arches_vue_utils/types";
import type {
    Concept,
    HeaderRefAndSetter,
    Labellable,
    Scheme,
} from "@/arches_lingo/types";

const { $gettext } = useGettext();
const router = useRouter();
const selectedLanguage = inject(selectedLanguageKey) as Ref<Language>;

const { setHeader } = inject(headerKey) as HeaderRefAndSetter;

const displayedRow: Ref<Labellable | null> = ref(null);
const rowLabel = computed(() => {
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
    if (dataIsScheme(val)) {
        router.push({ name: routeNames.scheme, params: { id: val.id } });
    } else if (dataIsConcept(val)) {
        router.push({ name: routeNames.concept, params: { id: val.id } });
    }
    setHeader(rowLabel.value);
};
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
            <ConceptDetail
                v-if="displayedRow && dataIsConcept(displayedRow)"
                :concept="displayedRow as Concept"
            />
            <SchemeDetail
                v-else-if="displayedRow && dataIsScheme(displayedRow)"
                :scheme="displayedRow as Scheme"
            />
        </SplitterPanel>
    </Splitter>
</template>
