<script setup lang="ts">
import { computed, inject, onMounted, ref, toRaw, type Ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useGettext } from "vue3-gettext";
import { useToast } from "primevue/usetoast";
import Button from "primevue/button";
import MetaStringViewer from "@/arches_lingo/components/generic/MetaStringViewer.vue";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
import {
    createScheme,
    fetchSchemeRights,
    createSchemeRights,
    updateSchemeRights,
    createSchemeRightStatement,
    updateSchemeRightStatement,
    deleteSchemeRightStatement,
    fetchPersonRdmSystemList,
    fetchGroupRdmSystemList,
} from "@/arches_lingo/api.ts";
import { fetchLists } from "@/arches_references/api.ts";

import type {
    ControlledListResult,
    ControlledListItem,
    ControlledListItemResult,
    DataComponentMode,
    MetaStringText,
    ResourceInstanceReference,
    ResourceInstanceResult,
    SchemeInstance,
    SchemeRights,
    SchemeRightStatement,
} from "@/arches_lingo/types";
import {
    selectedLanguageKey,
    NEW,
    ERROR,
    VIEW,
    EDIT,
    OPEN_EDITOR,
    UPDATED,
} from "@/arches_lingo/constants.ts";
import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";
import ReferenceDatatype from "@/arches_lingo/components/generic/ReferenceDatatype.vue";
import type { Language } from "@/arches_vue_utils/types.ts";
import NonLocalizedString from "../../generic/NonLocalizedString.vue";

onMounted(async () => {
    getActorOptions();
    getControlledLists();
    getSectionValue();
});

const emit = defineEmits([OPEN_EDITOR, UPDATED]);

const route = useRoute();
const router = useRouter();
const toast = useToast();
const { $gettext } = useGettext();

const actorRdmOptions = ref<ResourceInstanceReference[]>();
const selectedLanguage = inject(selectedLanguageKey) as Ref<Language>;
const rightTypeOptions = ref<ControlledListItem[]>();
const languageOptions = ref<ControlledListItem[]>();
const noteOptions = ref<ControlledListItem[]>();
const metatypesOptions = ref<ControlledListItem[]>();
const parentExists = ref(false);

const props = withDefaults(
    defineProps<{
        mode?: DataComponentMode;
        tileId?: string | null;
        args?: Array<object>;
    }>(),
    {
        mode: VIEW,
        tileId: null, // editor arg specifying what tile to operate on.
    },
);

const schemeRights = ref<SchemeRights>();
const schemeRightStatement = ref<SchemeRightStatement>();
const rightsTileId = ref<string>();
const rightStatementTileId = ref<string>();

const referenceNodeConfig = [
{
        nodeAlias: "appellative_status_status",
        listRef: rightTypeOptions,
        listName: "Right Types",
    },
    {
        nodeAlias: "appellative_status_ascribed_name_language",
        listRef: languageOptions,
        listName: "Languages",
    },
    {
        nodeAlias: "appellative_status_ascribed_relation",
        listRef: noteOptions,
        listName: "note",
    },
    {
        nodeAlias: "appellative_status_status_metatype",
        listRef: metatypesOptions,
        listName: "Metatypes",
    },
];

async function getActorOptions() {
    const options_person = await fetchPersonRdmSystemList();
    const options_group = await fetchGroupRdmSystemList();
    const options = options_person.concat(options_group);

    actorRdmOptions.value = options.map((option: ResourceInstanceResult) => {
        const result: ResourceInstanceReference = {
            display_value: option.descriptors[selectedLanguage.value.code].name,
            resourceId: option.resourceinstanceid,
            ontologyProperty: "ac41d9be-79db-4256-b368-2f4559cfbe55",
            inverseOntologyProperty: "ac41d9be-79db-4256-b368-2f4559cfbe55",
        };
        return result;
    });
}

async function getControlledLists() {
    let parsed;
    try {
        parsed = await fetchLists(
            referenceNodeConfig.map((node) => node.nodeAlias),
        );
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
    const controlledLists = parsed.controlled_lists;
    referenceNodeConfig.forEach((node) => {
        const matchingList = controlledLists.find(
            (list: ControlledListResult) => list.name === node.listName,
        );
        const options = matchingList.items.map(
            (item: ControlledListItemResult): ControlledListItem => ({
                list_id: item.list_id,
                uri: item.uri,
                labels: item.values,
            }),
        );
        node.listRef.value = options;
    });
}

function onUpdateResourceInstance(
    node: keyof SchemeRights,
    val: string[],
    options: ResourceInstanceReference[],
) {
    if (val.length > 0) {
        const selectedOptions = options.filter((option) =>
            val.includes(option.resourceId),
        );
        (schemeRights.value[node] as unknown) = selectedOptions;
    }
}

function onUpdateSchemeRightReferenceDatatype(
    node: keyof SchemeRights,
    val: ControlledListItem[],
) {
    (schemeRights.value[node] as unknown) = val.map((item) => toRaw(item));
}

function onUpdateSchemeRightStatementReferenceDatatype(
    node: keyof SchemeRightStatement,
    val: ControlledListItem[],
) {
    (schemeRightStatement.value[node] as unknown) = val.map((item) => toRaw(item));
}

function onUpdateString(node: keyof SchemeRightStatement, val: string) {
    (schemeRightStatement.value[node] as unknown) = toRaw(val);
}

async function saveRights() {
    try {
        if (route.params.id === NEW) {
            const newSchemeInstance: SchemeInstance = {
                rights: [toRaw(schemeRights.value)],
            };
            const updated = await createScheme(newSchemeInstance);
            await router.push({
                name: "scheme",
                params: { id: updated.resourceinstanceid },
            });
        } else if (!schemeRights.value?.tileid) {
            await createSchemeRights(route.params.id as string, schemeRights.value ?? {});
        } else {
            await updateSchemeRights(
                route.params.id as string,
                schemeRights.value?.tileid as string,
                schemeRights.value as SchemeRights,
            );
        }
        emit(UPDATED);
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error saving scheme"),
            detail: (error as Error).message,
        });
    }
}

async function getSectionValue() {
    if (route.params.id === NEW) {
        return;
    }
    const schemeInstance = await fetchSchemeRights(route.params.id as string);
    rightsTileId.value = schemeInstance?.rights?.tileid ?? '';
    rightStatementTileId.value = schemeInstance?.right_statement?.tileid ?? '';
    schemeRights.value = schemeInstance?.rights ?? {};
    if (schemeInstance?.rights) {
        parentExists.value = true;
    }
    schemeRightStatement.value = schemeInstance?.right_statement;
}

defineExpose({ getSectionValue });
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
                    :value="schemeRights?.right_holder"
                    :mode=VIEW
                />
                <h4>{{ $gettext('Rights Type') }}</h4>
                <ReferenceDatatype
                    :value="schemeRights?.right_type"
                    :mode=VIEW
                />
                <h4>{{ $gettext('Rights Statement') }}</h4>
                <NonLocalizedString
                    :value="schemeRightStatement?.right_statement_content"
                    :mode="VIEW"
                ></NonLocalizedString>
                <h4>{{ $gettext('Right Statement Language') }}</h4>
                <ReferenceDatatype
                    :value="schemeRightStatement?.right_statement_language"
                    :mode="VIEW"
                ></ReferenceDatatype>
                <h4>{{ $gettext('Right Statement Type') }}</h4>
                <ReferenceDatatype
                    :value="schemeRightStatement?.right_statement_type"
                    :mode="VIEW"
                ></ReferenceDatatype>
                <h4>{{ $gettext("Right Statement Type Metatype") }}</h4>
                <ReferenceDatatype
                    :value="schemeRightStatement?.right_statement_type_metatype"
                    :mode="VIEW"
                ></ReferenceDatatype>
                <h4>{{ $gettext("Right Statement Label") }}</h4>
                <NonLocalizedString
                    :value="schemeRightStatement?.right_statement_label"
                    :mode="VIEW"
                ></NonLocalizedString>
            </SchemeReportSection>
        </div>
        <div v-if="mode === EDIT">
            <div>
                <h4>{{ $gettext('Rights Holders') }}</h4>
                <ResourceInstanceRelationships
                    :value="schemeRights?.right_holder"
                    :options="actorRdmOptions"
                    :mode="EDIT"
                    @update="(val) => onUpdateResourceInstance('right_holder', val, actorRdmOptions ?? [])"
                />
                <h4>{{ $gettext('Rights Type') }}</h4>
                <ReferenceDatatype
                    :value="schemeRights?.right_type"
                    :options="rightTypeOptions"
                    :multi-value="false"
                    :mode="EDIT"
                    @update="(val) => onUpdateSchemeRightReferenceDatatype('right_type', val)"
                />
            </div>
            <div>
                <h4>{{ $gettext('Statement') }}</h4>
                <NonLocalizedString
                    :value="schemeRightStatement?.right_statement_content"
                    :mode="EDIT"
                    @update="
                        (val) =>
                            onUpdateString('right_statement_content', val)
                    "
                />
                <h4>{{ $gettext('Statement Language') }}</h4>
                <ReferenceDatatype
                    :value="schemeRightStatement?.right_statement_language"
                    :mode="EDIT"
                    :multi-value="false"
                    :options="languageOptions"
                    @update="
                        (val) =>
                            onUpdateSchemeRightStatementReferenceDatatype(
                                'right_statement_language',
                                val,
                            )
                    "
                />
                <h4>{{ $gettext('Statement Type') }}</h4>
                <ReferenceDatatype
                    :value="schemeRightStatement?.right_statement_type"
                    :mode="EDIT"
                    :multi-value="false"
                    :options="noteOptions"
                    @update="
                        (val) =>
                            onUpdateSchemeRightStatementReferenceDatatype(
                                'right_statement_type',
                                val,
                            )
                    "
                />
                <h4>{{ $gettext('Statement Type Metatype') }}</h4>
                <ReferenceDatatype
                    :value="schemeRightStatement?.right_statement_type_metatype"
                    :mode="EDIT"
                    :multi-value="false"
                    :options="metatypesOptions"
                    @update="
                        (val) => onUpdateSchemeRightStatementReferenceDatatype(
                            'right_statement_type_metatype',
                            val
                        )
                    "
                />
                <Button
                    :label="$gettext('Update')"
                    @click="saveRights"
                ></Button>
            </div>
        </div>
    </div>
</template>
