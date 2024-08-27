<script setup lang="ts">
import { provide, ref } from "vue";
import { useGettext } from "vue3-gettext";

import Panel from "primevue/panel";
import ProgressSpinner from "primevue/progressspinner";

import {
    displayedRowKey,
    selectedLanguageKey,
} from "@/arches_references/constants.ts";
import { ENGLISH } from "@/arches_lingo/constants.ts";
import { bestLabel } from "@/arches_lingo/utils.ts";
import ConceptTree from "@/arches_lingo/components/tree/ConceptTree.vue";

import type { Ref } from "vue";
import type { Language } from "@/arches/types";
import type { Labellable } from "@/arches_lingo/types.ts";

const { $gettext } = useGettext();

// TODO: lift some of this state up?
const displayedRow: Ref<Labellable | null> = ref(null);
const setDisplayedRow = (val: Labellable | null) => {
    displayedRow.value = val;
    // TODO: routing
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
                : "") || "Schemes list placeholder"
        }}
    </div>
</template>
