<script setup lang="ts">
import { provide, ref } from "vue";
import { useRouter } from "vue-router";
import { useGettext } from "vue3-gettext";

import Panel from "primevue/panel";
import ProgressSpinner from "primevue/progressspinner";

import {
    displayedRowKey,
    selectedLanguageKey,
} from "@/arches_references/constants.ts";
import { ENGLISH } from "@/arches_lingo/constants.ts";
import { routeNames } from "@/arches_lingo/routes.ts";
import { bestLabel, dataIsConcept } from "@/arches_lingo/utils.ts";
import ConceptTree from "@/arches_lingo/components/tree/ConceptTree.vue";

import type { Ref } from "vue";
import type { Language } from "@/arches/types";
import type { Labellable } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();
const router = useRouter();

// TODO: lift some of this state up?
const displayedRow: Ref<Labellable | null> = ref(null);
const setDisplayedRow = (val: Labellable | null) => {
    displayedRow.value = val;
    if (val === null) {
        return;
    }
    if (dataIsConcept(val)) {
        router.push({ name: routeNames.concept, params: { id: val.id } });
    }
};
provide(displayedRowKey, { displayedRow, setDisplayedRow });

const selectedLanguage: Ref<Language> = ref(ENGLISH);
provide(selectedLanguageKey, selectedLanguage);
</script>

<template>
    <div style="display: flex; flex-direction: row; gap: 1rem">
        <Panel
            toggleable
            :header="$gettext('Hierarchy')"
            :pt="{
                pcToggleButton: {
                    root: {
                        ariaLabel: $gettext('Expand or collapse hierarchy'),
                    },
                },
            }"
        >
            <Suspense>
                <ConceptTree />
                <template #fallback>
                    <ProgressSpinner />
                </template>
            </Suspense>
        </Panel>
        {{
            (displayedRow
                ? bestLabel(displayedRow, selectedLanguage.code).value
                : "") || "Concept detail placeholder"
        }}
    </div>
</template>
