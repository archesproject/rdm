<script lang="ts">
const OPEN_EDITOR = "openEditor";
</script>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useGettext } from "vue3-gettext";

import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
import NonLocalizedString from "@/arches_lingo/components/generic/NonLocalizedString.vue";
import {
    fetchSchemeNamespace,
    updateSchemeNamespace,
} from "@/arches_lingo/api.ts";
import type {
    DataComponentMode,
    SchemeNamespaceUpdate,
    SchemeNamespace,
} from "@/arches_lingo/types";

const { $gettext } = useGettext();
const schemeNamespace = ref<SchemeNamespace>();
const route = useRoute();

defineProps<{
    mode?: DataComponentMode;
}>();

defineEmits([OPEN_EDITOR]);

defineExpose({ save, getSectionValue });

onMounted(async () => {
    getSectionValue();
});

async function save() {
    await updateSchemeNamespace(
        route.params.id as string,
        schemeNamespace.value as SchemeNamespace,
    );
}

async function getSectionValue() {
    const response = await fetchSchemeNamespace(route.params.id as string);
    schemeNamespace.value = response;
}

const onNamespaceNameUpdate = (val: string) => {
    const namespaceValue = schemeNamespace.value as SchemeNamespaceUpdate;
    if (!namespaceValue?.namespace) {
        namespaceValue.namespace = {
            namespace_name: val,
            namespace_type: [{ value: "namespace" }],
        };
    } else {
        namespaceValue.namespace.namespace_name = val;
        namespaceValue.namespace.namespace_type = [{ value: "namespace" }];
    }
};
</script>

<template>
    <div>
        <div v-if="!mode || mode === 'view'">
            <SchemeReportSection
                :title-text="$gettext('Scheme Namespace')"
                @open-editor="$emit(OPEN_EDITOR)"
            >
                <NonLocalizedString
                    :value="schemeNamespace?.namespace?.namespace_name"
                    mode="view"
                />
                <!-- Discussion of namespace_type indicated it should not be displayed or edited manually,
                 if this changes, the ControlledListItem widget can be used.-->
            </SchemeReportSection>
        </div>
        <div v-if="mode === 'edit'">
            <NonLocalizedString
                :value="schemeNamespace?.namespace?.namespace_name ?? ''"
                mode="edit"
                @update="onNamespaceNameUpdate"
            />
        </div>
    </div>
</template>
