<script setup lang="ts">
import { inject, onMounted, ref, toRaw, type Ref } from "vue";
import { useRoute } from "vue-router";
import { useGettext } from "vue3-gettext";
import Button from "primevue/button";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
import {
    fetchSchemeRights,
    updateSchemeRights,
    fetchPersonRdmSystemList,
    fetchGroupRdmSystemList,
    fetchControlledListOptions,
} from "@/arches_lingo/api.ts";
import type {
    DataComponentMode,
    ResourceInstanceReference,
    ResourceInstanceResult,
    ControlledListItem,
    ControlledListItemResult,
    SchemeRights,
} from "@/arches_lingo/types";
import {
    selectedLanguageKey,
    VIEW,
    EDIT,
    OPEN_EDITOR,
    UPDATED,
    RIGHT_TYPE_CONTROLLED_LIST,
} from "@/arches_lingo/constants.ts";
import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";
import ReferenceDatatype from "@/arches_lingo/components/generic/ReferenceDatatype.vue";
import type { Language } from "@/arches_vue_utils/types.ts";

onMounted(async () => {
    getSectionValue();
});

defineProps<{
    mode?: DataComponentMode;
}>();

const emit = defineEmits([OPEN_EDITOR, UPDATED]);

const schemeRight = ref<SchemeRights>();
const tileid = ref<string>();
const route = useRoute();
const actorRdmOptions = ref<ResourceInstanceReference[]>();
const selectedLanguage = inject(selectedLanguageKey) as Ref<Language>;
const rightTypeOptions = ref<ControlledListItem[]>();

async function getActorOptions(): Promise<ResourceInstanceReference[]> {
    const options_person = await fetchPersonRdmSystemList();
    const options_group = await fetchGroupRdmSystemList();
    const options = options_person.concat(options_group);

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
};
async function getControlledListOptions(listId: string): Promise<ControlledListItem[]> {
    const parsed = await fetchControlledListOptions(listId);
    const options = parsed.items.map(
        (item: ControlledListItemResult): ControlledListItem => ({
            list_id: item.list_id,
            uri: item.uri,
            labels: item.values
        }),
    );
    return options;
};

function onUpdateReferenceDatatype(
    node: keyof SchemeRights,
    val: ControlledListItem[],
) {
    (schemeRight.value[node] as unknown) = val.map((item) => toRaw(item));
};

function onUpdateResourceInstance(
    node: keyof SchemeRights,
    val: string[],
    options: ResourceInstanceReference[],
) {
    if (val.length > 0) {
        const selectedOptions = options.filter((option) =>
            val.includes(option.resourceId),
        );
        (schemeRight.value[node] as unknown) = selectedOptions;
    }
};

async function save() {
    await updateSchemeRights(
        route.params.id as string,
        tileid.value as string,
        schemeRight.value as SchemeRights,
    );
    emit(UPDATED);
};
async function getSectionValue() {
    const actorOptions = await getActorOptions();
    const scheme = await fetchSchemeRights(route.params.id as string);
    schemeRight.value = scheme?.rights;
    tileid.value = schemeRight.value?.tileid;
    actorRdmOptions.value = actorOptions.map((option) => {
        const savedSource = schemeRight.value?.right_holder?.find(
            (source: ResourceInstanceReference) =>
                source.resourceId === option.resourceId,
        );
        if (savedSource) {
            return savedSource;
        } else {
            return option;
        }
    });
    rightTypeOptions.value = await getControlledListOptions(RIGHT_TYPE_CONTROLLED_LIST);
};

defineExpose({ getSectionValue });
const { $gettext } = useGettext();
</script>

<template>
    <div>
        <div v-if="!mode || mode === VIEW">
            <SchemeReportSection
                :title-text="$gettext('Scheme Rights')"
                :button-text="$gettext('Update Scheme Rights')"
                @open-editor="$emit(OPEN_EDITOR)"
            >
                <h4>{{ $gettext('Rights Holders') }}</h4>
                <ResourceInstanceRelationships
                    :value="schemeRight?.right_holder"
                    :mode=VIEW
                />
                <h4>{{ $gettext('Rights Type') }}</h4>
                <ReferenceDatatype
                    :value="schemeRight?.right_type"
                    :mode=VIEW
                />
            </SchemeReportSection>
        </div>
        <div v-if="mode === EDIT">
            <h4>{{ $gettext('Rights Holders') }}</h4>
            <ResourceInstanceRelationships
                :value="schemeRight?.right_holder"
                :options="actorRdmOptions"
                :mode="EDIT"
                @update="(val) => onUpdateResourceInstance('right_holder', val, actorRdmOptions ?? [])"
            />
            <h4>{{ $gettext('Rights Type') }}</h4>
            <ReferenceDatatype
                :value="schemeRight?.right_type"
                :options="rightTypeOptions"
                :multi-value="false"
                :mode="EDIT"
                @update="(val) => onUpdateReferenceDatatype('right_type', val)"
            />
            <Button
                :label="$gettext('Update')"
                @click="save"
            ></Button>
        </div>
    </div>
</template>
