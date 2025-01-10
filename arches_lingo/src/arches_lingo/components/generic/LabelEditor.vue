<script setup lang="ts">
import { computed, inject, onMounted, ref, toRaw, toRef, type Ref } from "vue";

import Button from "primevue/button";
import { useGettext } from "vue3-gettext";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "primevue/usetoast";

import {
    createScheme,
    createSchemeLabel,
    fetchControlledListOptions,
    fetchGroupRdmSystemList,
    fetchPersonRdmSystemList,
    fetchTextualWorkRdmSystemList,
    updateSchemeLabel,
} from "@/arches_lingo/api.ts";

import DateDatatype from "@/arches_lingo/components/generic/DateDatatype.vue";
import NonLocalizedString from "@/arches_lingo/components/generic/NonLocalizedString.vue";
import ReferenceDatatype from "@/arches_lingo/components/generic/ReferenceDatatype.vue";
import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";

import {
    EDIT,
    ERROR,
    EVENT_TYPES_CONTROLLED_LIST,
    LABEL_CONTROLLED_LIST,
    LANGUAGE_CONTROLLED_LIST,
    METATYPES_CONTROLLED_LIST,
    NEW,
    selectedLanguageKey,
    STATUSES_CONTROLLED_LIST,
} from "@/arches_lingo/constants.ts";

import type {
    AppellativeStatus,
    ControlledListItem,
    ControlledListItemResult,
    ResourceInstanceReference,
    ResourceInstanceResult,
    SchemeInstance,
} from "@/arches_lingo/types.ts";
import type { Language } from "@/arches_vue_utils/types.ts";

const emit = defineEmits(["update"]);
const toast = useToast();
const route = useRoute();
const router = useRouter();
const selectedLanguage = inject(selectedLanguageKey) as Ref<Language>;
const { $gettext } = useGettext();

const props = withDefaults(
    defineProps<{
        value?: AppellativeStatus;
    }>(),
    {
        value: () => ({}) as AppellativeStatus,
    },
);
const valueRef = toRef(props, "value");
const formValue = computed({
    get: () => valueRef.value,
    set: (newVal: AppellativeStatus) => {
        valueRef.value = newVal;
    },
});

const languageOptions = ref<ControlledListItem[]>([]);
const typeOptions = ref<ControlledListItem[]>([]);
const statusOptions = ref<ControlledListItem[]>([]);
const metatypeOptions = ref<ControlledListItem[]>([]);
const eventTypeOptions = ref<ControlledListItem[]>([]);
const groupAndPersonOptions = ref<ResourceInstanceReference[]>();
const textualWorkOptions = ref<ResourceInstanceReference[]>();

function onUpdateString(node: keyof AppellativeStatus, val: string) {
    (formValue.value[node] as unknown) = toRaw(val);
}

function onUpdateReferenceDatatype(
    node: keyof AppellativeStatus,
    val: ControlledListItem[],
) {
    (formValue.value[node] as unknown) = val.map((item) => toRaw(item));
}

function onUpdateResourceInstance(
    node: keyof AppellativeStatus,
    val: string[],
    options: ResourceInstanceReference[],
) {
    if (val.length > 0) {
        const selectedOptions = options.filter((option) =>
            val.includes(option.resourceId),
        );
        (formValue.value[node] as unknown) = selectedOptions;
    }
}

async function save() {
    try {
        if (route.params.id === NEW) {
            const newSchemeInstance: SchemeInstance = {
                appellative_status: [toRaw(formValue.value)],
            };
            const updated = await createScheme(newSchemeInstance);
            await router.push({
                name: "scheme",
                params: { id: updated.resourceinstanceid },
            });
        } else if (!formValue.value.tileid) {
            await createSchemeLabel(route.params.id as string, formValue.value);
        } else {
            await updateSchemeLabel(
                route.params.id as string,
                formValue.value.tileid,
                formValue.value,
            );
        }
        emit("update");
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error saving scheme"),
            detail: (error as Error).message,
        });
    }
}

async function getControlledListOptions(
    listId: string,
): Promise<ControlledListItem[]> {
    let parsed;
    try {
        parsed = await fetchControlledListOptions(listId);
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail:
                error instanceof Error
                    ? error.message
                    : $gettext("Could not fetch the controlled list options"),
        });
        return [];
    }
    const options = parsed.items.map(
        (item: ControlledListItemResult): ControlledListItem => ({
            list_id: item.list_id,
            uri: item.uri,
            labels: item.values,
        }),
    );
    return options;
}

async function getResourceInstanceOptions(
    fetchOptions: () => Promise<ResourceInstanceResult[]>,
): Promise<ResourceInstanceReference[]> {
    let options;
    try {
        options = await fetchOptions();
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail:
                error instanceof Error
                    ? error.message
                    : $gettext("Could not fetch the resource instance options"),
        });
        return [];
    }
    const results = options.map((option: ResourceInstanceResult) => {
        const result: ResourceInstanceReference = {
            display_value: option.descriptors[selectedLanguage.value.code].name,
            resourceId: option.resourceinstanceid,
            ontologyProperty: "ac41d9be-79db-4256-b368-2f4559cfbe55",
            inverseOntologyProperty: "ac41d9be-79db-4256-b368-2f4559cfbe55",
        };
        return result;
    });
    return results;
}

onMounted(async () => {
    const [languageOpts, typeOpts, statusOpts, metatypeOpts, eventTypeOpts] =
        await Promise.all([
            getControlledListOptions(LANGUAGE_CONTROLLED_LIST),
            getControlledListOptions(LABEL_CONTROLLED_LIST),
            getControlledListOptions(STATUSES_CONTROLLED_LIST),
            getControlledListOptions(METATYPES_CONTROLLED_LIST),
            getControlledListOptions(EVENT_TYPES_CONTROLLED_LIST),
        ]);

    languageOptions.value = languageOpts;
    typeOptions.value = typeOpts;
    statusOptions.value = statusOpts;
    metatypeOptions.value = metatypeOpts;
    eventTypeOptions.value = eventTypeOpts;
    groupAndPersonOptions.value = await getResourceInstanceOptions(
        fetchGroupRdmSystemList,
    );
    groupAndPersonOptions.value = [
        ...(groupAndPersonOptions.value || []),
        ...(await getResourceInstanceOptions(fetchPersonRdmSystemList)),
    ];
    textualWorkOptions.value = await getResourceInstanceOptions(
        fetchTextualWorkRdmSystemList,
    );
});
</script>

<template>
    <!-- Label: string -->
    <label for="">{{ $gettext("Label") }}</label>
    <NonLocalizedString
        :value="formValue?.appellative_status_ascribed_name_content"
        :mode="EDIT"
        @update="
            (val) =>
                onUpdateString('appellative_status_ascribed_name_content', val)
        "
    />
    <!-- Label Language: reference datatype -->
    <label for="">{{ $gettext("Label Language") }}</label>
    <ReferenceDatatype
        :value="formValue?.appellative_status_ascribed_name_language"
        :mode="EDIT"
        :multi-value="false"
        :options="languageOptions"
        @update="
            (val) =>
                onUpdateReferenceDatatype(
                    'appellative_status_ascribed_name_language',
                    val,
                )
        "
    />
    <!-- Label Type: reference datatype -->
    <label for="">{{ $gettext("Label Type") }}</label>
    <ReferenceDatatype
        :value="formValue?.appellative_status_ascribed_relation"
        :mode="EDIT"
        :multi-value="false"
        :options="typeOptions"
        @update="
            (val) =>
                onUpdateReferenceDatatype(
                    'appellative_status_ascribed_relation',
                    val,
                )
        "
    />
    <!-- Label Status: reference datatype -->
    <label for="">{{ $gettext("Label Status") }}</label>
    <ReferenceDatatype
        :value="formValue?.appellative_status_status"
        :mode="EDIT"
        :multi-value="false"
        :options="statusOptions"
        @update="
            (val) => onUpdateReferenceDatatype('appellative_status_status', val)
        "
    />
    <!-- Label Status Metatype: reference datatype -->
    <label for="">{{ $gettext("Label Metatype") }}</label>
    <ReferenceDatatype
        :value="formValue?.appellative_status_status_metatype"
        :mode="EDIT"
        :multi-value="false"
        :options="metatypeOptions"
        @update="
            (val) =>
                onUpdateReferenceDatatype(
                    'appellative_status_status_metatype',
                    val,
                )
        "
    />

    <!-- Label Temporal Validity Start: date -->
    <label for="">{{ $gettext("Label Temporal Validity Start") }}</label>
    <DateDatatype
        :value="formValue?.appellative_status_timespan_begin_of_the_begin"
        :mode="EDIT"
        @update="
            (val) =>
                onUpdateString(
                    'appellative_status_timespan_begin_of_the_begin',
                    val,
                )
        "
    />

    <!-- Label Temporal Validity End: date -->
    <label for="">{{ $gettext("Label Temporal Validity End") }}</label>
    <DateDatatype
        :value="formValue?.appellative_status_timespan_end_of_the_end"
        :mode="EDIT"
        @update="
            (val) =>
                onUpdateString(
                    'appellative_status_timespan_end_of_the_end',
                    val,
                )
        "
    />

    <!-- Contributor: resource instance -->
    <label for="">{{ $gettext("Contributor") }}</label>
    <ResourceInstanceRelationships
        :value="formValue?.appellative_status_data_assignment_actor"
        :mode="EDIT"
        :options="groupAndPersonOptions"
        @update="
            (val) =>
                onUpdateResourceInstance(
                    'appellative_status_data_assignment_actor',
                    val,
                    groupAndPersonOptions ?? [],
                )
        "
    />
    <!-- Sources: resource instance -->
    <label for="">{{ $gettext("Sources") }}</label>
    <ResourceInstanceRelationships
        :value="formValue?.appellative_status_data_assignment_object_used"
        :mode="EDIT"
        :options="textualWorkOptions"
        @update="
            (val) =>
                onUpdateResourceInstance(
                    'appellative_status_data_assignment_object_used',
                    val,
                    textualWorkOptions ?? [],
                )
        "
    />
    <!-- Warrant Type: reference datatype -->
    <label for="">{{ $gettext("Warrant Type") }}</label>
    <ReferenceDatatype
        :value="formValue?.appellative_status_data_assignment_type"
        :mode="EDIT"
        :multi-value="false"
        :options="eventTypeOptions"
        @update="
            (val) =>
                onUpdateReferenceDatatype(
                    'appellative_status_data_assignment_type',
                    val,
                )
        "
    />
    <Button
        :label="$gettext('Update')"
        @click="save"
    ></Button>
</template>
