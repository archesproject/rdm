<script setup lang="ts">
import { defineProps, onMounted, ref } from "vue";
import { fetchControlledListOptions } from "@/arches_lingo/api.ts";

import NonLocalizedString from "@/arches_lingo/components/generic/NonLocalizedString.vue";
import ReferenceDatatype from "@/arches_lingo/components/generic/ReferenceDatatype.vue";
// import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";

import { EDIT, LANGUAGE_CONTROLLED_LIST } from "@/arches_lingo/constants.ts";

import type {
    AppellativeStatus,
    ControlledListItem,
    ControlledListItemResult,
} from "@/arches_lingo/types.ts";

const props = withDefaults(
    defineProps<{
        value?: AppellativeStatus;
    }>(),
    {
        value: () => ({}) as AppellativeStatus,
    },
);
const appellative_status = ref(props.value);

function onUpdate(newValue: string) {
    // handle the update
    console.log("Update new value here!" + newValue);
}

async function getOptions(listId: string): Promise<ControlledListItem[]> {
    const parsed = await fetchControlledListOptions(listId);
    const options = parsed.items.map(
        (item: ControlledListItemResult): ControlledListItem => ({
            list_id: item.list_id,
            uri: item.uri,
            labels: item.values,
        }),
    );
    return options;
}

const languageOptions = ref<ControlledListItem[]>([]);

onMounted(async () => {
    const lang_opts = await getOptions(LANGUAGE_CONTROLLED_LIST);
    languageOptions.value = lang_opts;
});
</script>

<template>
    <!-- Label: string -->
    <label for="">{{ $gettext("Label") }}</label>
    <NonLocalizedString
        :value="
            appellative_status?.appellative_status_ascribed_name_content ?? ''
        "
        :mode="EDIT"
        @update="onUpdate"
    />
    <!-- Label Language: reference datatype -->
    <label for="">{{ $gettext("Label Language") }}</label>
    <ReferenceDatatype
        :value="appellative_status?.appellative_status_ascribed_name_language"
        :mode="EDIT"
        :multivalue="false"
        :options="languageOptions"
    />
    <!-- Label Type: reference datatype -->
    <label for="">{{ $gettext("Label Type") }}</label>

    <!-- Label Status: reference datatype -->
    <label for="">{{ $gettext("Label Status") }}</label>

    <!-- Label Status Metatype: reference datatype -->
    <label for="">{{ $gettext("Label Metatype") }}</label>

    <!-- Label Temporal Validity Start: date -->
    <label for="">{{ $gettext("Label Temporal Validity Start") }}</label>

    <!-- Label Temporal Validity End: date -->
    <label for="">{{ $gettext("Label Temporal Validity End") }}</label>

    <!-- Contributor: resource instance -->
    <label for="">{{ $gettext("Contributor") }}</label>

    <!-- Sources: resource instance -->
    <label for="">{{ $gettext("Sources") }}</label>

    <!-- Warrant Type: reference datatype -->
    <label for="">{{ $gettext("Warrant Type") }}</label>
</template>
