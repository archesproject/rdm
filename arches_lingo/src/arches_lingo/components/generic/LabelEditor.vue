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
const formId = (route.params.id as string) ?? Math.random().toString();

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
    <label :for="formId + '-label'">{{ $gettext("Label") }}</label>
    <NonLocalizedString
        :value="formValue?.appellative_status_ascribed_name_content"
        :mode="EDIT"
        :pt-id="formId + '-label'"
        @update="
            (val) =>
                onUpdateString('appellative_status_ascribed_name_content', val)
        "
    />
    <p :id="formId + '-label-language'">{{ $gettext("Label Language") }}</p>
    <ReferenceDatatype
        :value="formValue?.appellative_status_ascribed_name_language"
        :mode="EDIT"
        :multi-value="false"
        :options="languageOptions"
        :pt-aria-labeled-by="formId + '-label-language'"
        @update="
            (val) =>
                onUpdateReferenceDatatype(
                    'appellative_status_ascribed_name_language',
                    val,
                )
        "
    />
    <p :id="formId + '-label-type'">{{ $gettext("Label Type") }}</p>
    <ReferenceDatatype
        :value="formValue?.appellative_status_ascribed_relation"
        :mode="EDIT"
        :multi-value="false"
        :options="typeOptions"
        :pt-aria-labeled-by="formId + '-label-type'"
        @update="
            (val) =>
                onUpdateReferenceDatatype(
                    'appellative_status_ascribed_relation',
                    val,
                )
        "
    />
    <p :id="formId + '-label-status'">{{ $gettext("Label Status") }}</p>
    <ReferenceDatatype
        :value="formValue?.appellative_status_status"
        :mode="EDIT"
        :multi-value="false"
        :options="statusOptions"
        :pt-aria-labeled-by="formId + '-label-status'"
        @update="
            (val) => onUpdateReferenceDatatype('appellative_status_status', val)
        "
    />
    <p :id="formId + '-label-metatype'">{{ $gettext("Label Metatype") }}</p>
    <ReferenceDatatype
        :value="formValue?.appellative_status_status_metatype"
        :mode="EDIT"
        :multi-value="false"
        :options="metatypeOptions"
        :pt-aria-labeled-by="formId + '-label-metatype'"
        @update="
            (val) =>
                onUpdateReferenceDatatype(
                    'appellative_status_status_metatype',
                    val,
                )
        "
    />
    <p :id="formId + '-label-start'">
        {{ $gettext("Label Temporal Validity Start") }}
    </p>
    <DateDatatype
        :value="formValue?.appellative_status_timespan_begin_of_the_begin"
        :mode="EDIT"
        :pt-aria-labeled-by="formId + '-label-start'"
        @update="
            (val) =>
                onUpdateString(
                    'appellative_status_timespan_begin_of_the_begin',
                    val,
                )
        "
    />
    <p :id="formId + '-label-end'">
        {{ $gettext("Label Temporal Validity End") }}
    </p>
    <DateDatatype
        :value="formValue?.appellative_status_timespan_end_of_the_end"
        :mode="EDIT"
        :pt-aria-labeled-by="formId + '-label-end'"
        @update="
            (val) =>
                onUpdateString(
                    'appellative_status_timespan_end_of_the_end',
                    val,
                )
        "
    />
    <p :id="formId + '-label-contributor'">{{ $gettext("Contributor") }}</p>
    <ResourceInstanceRelationships
        :value="formValue?.appellative_status_data_assignment_actor"
        :mode="EDIT"
        :options="groupAndPersonOptions"
        :pt-aria-labeled-by="formId + '-label-contributor'"
        @update="
            (val) =>
                onUpdateResourceInstance(
                    'appellative_status_data_assignment_actor',
                    val,
                    groupAndPersonOptions ?? [],
                )
        "
    />
    <p :id="formId + '-label-sources'">{{ $gettext("Sources") }}</p>
    <ResourceInstanceRelationships
        :value="formValue?.appellative_status_data_assignment_object_used"
        :mode="EDIT"
        :options="textualWorkOptions"
        :pt-aria-labeled-by="formId + '-label-sources'"
        @update="
            (val) =>
                onUpdateResourceInstance(
                    'appellative_status_data_assignment_object_used',
                    val,
                    textualWorkOptions ?? [],
                )
        "
    />
    <p :id="formId + '-label-warrant'">{{ $gettext("Warrant Type") }}</p>
    <ReferenceDatatype
        :value="formValue?.appellative_status_data_assignment_type"
        :mode="EDIT"
        :multi-value="false"
        :options="eventTypeOptions"
        :pt-aria-labeled-by="formId + '-label-warrant'"
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
<style scoped>
p {
    margin: 0;
}
</style>
