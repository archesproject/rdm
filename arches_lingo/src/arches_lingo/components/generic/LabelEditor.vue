<script setup lang="ts">
import { defineProps, onMounted, ref } from "vue";
import { fetchControlledListOptions } from "@/arches_lingo/api.ts";

import NonLocalizedString from "@/arches_lingo/components/generic/NonLocalizedString.vue";
import ReferenceDatatype from "@/arches_lingo/components/generic/ReferenceDatatype.vue";
// import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";

import {
    EDIT,
    LANGUAGE_CONTROLLED_LIST,
    LABEL_CONTROLLED_LIST,
    STATUSES_CONTROLLED_LIST,
    METATYPES_CONTROLLED_LIST,
    EVENT_TYPES_CONTROLLED_LIST,
} from "@/arches_lingo/constants.ts";

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
    console.log(newValue);
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
const typeOptions = ref<ControlledListItem[]>([]);
const statusOptions = ref<ControlledListItem[]>([]);
const metatypeOptions = ref<ControlledListItem[]>([]);
const eventTypeOptions = ref<ControlledListItem[]>([]);

onMounted(async () => {
    languageOptions.value = await getOptions(LANGUAGE_CONTROLLED_LIST);
    typeOptions.value = await getOptions(LABEL_CONTROLLED_LIST);
    statusOptions.value = await getOptions(STATUSES_CONTROLLED_LIST);
    metatypeOptions.value = await getOptions(METATYPES_CONTROLLED_LIST);
    eventTypeOptions.value = await getOptions(EVENT_TYPES_CONTROLLED_LIST);
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
        :multi-value="false"
        :options="languageOptions"
        @update="onUpdate"
    />
    <!-- Label Type: reference datatype -->
    <label for="">{{ $gettext("Label Type") }}</label>
    <ReferenceDatatype
        :value="appellative_status?.appellative_status_ascribed_relation"
        :mode="EDIT"
        :multi-value="false"
        :options="typeOptions"
        @update="onUpdate"
    />
    <!-- Label Status: reference datatype -->
    <label for="">{{ $gettext("Label Status") }}</label>
    <ReferenceDatatype
        :value="appellative_status?.appellative_status_status"
        :mode="EDIT"
        :multi-value="false"
        :options="statusOptions"
        @update="onUpdate"
    />
    <!-- Label Status Metatype: reference datatype -->
    <label for="">{{ $gettext("Label Metatype") }}</label>
    <ReferenceDatatype
        :value="appellative_status?.appellative_status_status_metatype"
        :mode="EDIT"
        :multi-value="false"
        :options="metatypeOptions"
        @update="onUpdate"
    />
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
    <ReferenceDatatype
        :value="appellative_status?.appellative_status_data_assignment_type"
        :mode="EDIT"
        :multi-value="false"
        :options="eventTypeOptions"
        @update="onUpdate"
    />
</template>
