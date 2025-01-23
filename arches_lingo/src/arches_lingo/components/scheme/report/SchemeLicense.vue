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
const editingStatement = ref(false);
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
const schemeRightStatement = ref<SchemeRightStatement[]>();
const rightsTileId = ref<string>();
const rightStatementTileId = ref<string>();
const selectedSchemeRightStatement = computed(() => {
        const selected = schemeRightStatement.value?.find(
            (tile) => tile.tileid === props.tileId
        );
        if (!selected) {
            return {} as SchemeRightStatement;
        } else { return selected; }
    },
);

const metaStringLabel: MetaStringText = {
    deleteConfirm: $gettext("Are you sure you want to delete this label?"),
    language: $gettext("Statement Language"),
    name: $gettext("Statement"),
    type: $gettext("Statement Type"),
    noRecords: $gettext("No scheme right statement were found."),
};

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
    (selectedSchemeRightStatement.value[node] as unknown) = val.map((item) => toRaw(item));
}

function onUpdateString(node: keyof SchemeRightStatement, val: string) {
    (selectedSchemeRightStatement.value[node] as unknown) = toRaw(val);
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

async function saveRightStatement() {
    if (!selectedSchemeRightStatement.value) {
        return;
    }
    try {
        if (!selectedSchemeRightStatement.value?.tileid) {
            await createSchemeRightStatement(
                route.params.id as string,
                rightStatementTileId.value ?? '',
                selectedSchemeRightStatement.value
            );
        } else {
            await updateSchemeRightStatement(
                route.params.id as string,
                selectedSchemeRightStatement.value.tileid as string,
                selectedSchemeRightStatement.value as SchemeRightStatement,
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
    if (schemeInstance?.right_statement && !Array.isArray(schemeInstance?.right_statement)) {
        schemeInstance.right_statement = [schemeInstance.right_statement];
    }
    schemeRights.value = schemeInstance?.rights ?? {};
    if (schemeInstance?.rights) {
        parentExists.value = true;
    }
    schemeRightStatement.value = schemeInstance?.right_statement;

    const actorOptions = await getActorOptions();
    actorRdmOptions.value = actorOptions.map((option) => {
        const savedSource = schemeRights.value?.right_holder?.find(
            (source: ResourceInstanceReference) =>
                source.resourceId === option.resourceId,
        );
        if (savedSource) {
            return savedSource;
        } else {
            return option;
        }
    });
    getControlledLists();
}

async function deleteStatementValue(tileId: string) {
    let result = false;
    try {
        result = await deleteSchemeRightStatement(route.params.id as string, tileId);
    } catch (error) {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail:
                error instanceof Error
                    ? error.message
                    : $gettext("Could not delete selected label"),
        });
    }

    if (result) {
        getSectionValue();
    }
}

function addStatementValue() {
    editingStatement.value = true;
}

function editStatementValue(tileId: string) {
    editingStatement.value = true;
    const selectedSchemeRightStatement = schemeRightStatement.value?.find(
        (tile) => tile.tileid === tileId,
    );

    if (selectedSchemeRightStatement && selectedSchemeRightStatement?.tileid === tileId) {
        emit(OPEN_EDITOR, selectedSchemeRightStatement?.tileid);
    } else {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail: $gettext("Could not find the selected statement to edit"),
        });
    }
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
                <h4>{{ $gettext('Rights Statements') }}</h4>
                <MetaStringViewer
                    :meta-strings="schemeRightStatement"
                    :meta-string-text="metaStringLabel"
                    @edit-string="editStatementValue"
                    @delete-string="deleteStatementValue"
                >
                    <template #name="{ rowData }">
                        <span>
                            {{
                                (rowData as SchemeRightStatement)
                                    .right_statement_content
                            }}
                        </span>
                    </template>
                    <template #type="{ rowData }">
                        <ReferenceDatatype
                            :value="
                                (rowData as SchemeRightStatement)
                                    .right_statement_type
                            "
                            :mode="VIEW"
                        >
                        </ReferenceDatatype>
                    </template>
                    <template #language="{ rowData }">
                        <ReferenceDatatype
                            :value="
                                (rowData as SchemeRightStatement)
                                    .right_statement_language
                            "
                            :mode="VIEW"
                        >
                        </ReferenceDatatype>
                    </template>
                    <template #drawer="{ rowData }">
                        <div>
                            <span>{{ $gettext("Right Statement Label:") }}</span>
                            <NonLocalizedString
                                :value="
                                    (rowData as SchemeRightStatement)
                                        .right_statement_label
                                "
                                :mode="VIEW"
                            ></NonLocalizedString>
                        </div>
                        <div>
                            <span>{{ $gettext("Right Statement Type Metatype:") }}</span>
                            <ReferenceDatatype
                                :value="
                                    (rowData as SchemeRightStatement)
                                        .right_statement_type_metatype
                                "
                                :mode="VIEW"
                            ></ReferenceDatatype>
                        </div>
                    </template>
                </MetaStringViewer>
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
                <Button
                    :label="$gettext('Update')"
                    @click="saveRights"
                ></Button>
                <Button
                    if-show="parentExists"
                    :label="$gettext('Add Scheme Right Statement')"
                    @click="addStatementValue"
                ></Button>
            </div>
            <div v-show="editingStatement">
                <h4>{{ $gettext('Statement') }}</h4>
                <NonLocalizedString
                    :value="selectedSchemeRightStatement?.right_statement_content"
                    :mode="EDIT"
                    @update="
                        (val) =>
                            onUpdateString('right_statement_content', val)
                    "
                />
                <h4>{{ $gettext('Statement Language') }}</h4>
                <ReferenceDatatype
                    :value="selectedSchemeRightStatement?.right_statement_language"
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
                    :value="selectedSchemeRightStatement?.right_statement_type"
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
                    :value="selectedSchemeRightStatement?.right_statement_type_metatype"
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
                    @click="saveRightStatement"
                ></Button>
            </div>
        </div>
    </div>
</template>
