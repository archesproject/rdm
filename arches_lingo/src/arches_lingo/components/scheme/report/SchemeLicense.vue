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
    fetchControlledListOptions,
} from "@/arches_lingo/api.ts";
import type {
    ControlledListItem,
    ControlledListItemResult,
    DataComponentMode,
    MetaStringText,
    ResourceInstanceReference,
    ResourceInstanceResult,
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
    RIGHT_TYPE_CONTROLLED_LIST,
    METATYPES_CONTROLLED_LIST,
    LANGUAGE_CONTROLLED_LIST,
    NOTE_CONTROLLED_LIST,
} from "@/arches_lingo/constants.ts";
import ResourceInstanceRelationships from "@/arches_lingo/components/generic/ResourceInstanceRelationships.vue";
import ReferenceDatatype from "@/arches_lingo/components/generic/ReferenceDatatype.vue";
import type { Language } from "@/arches_vue_utils/types.ts";
import NonLocalizedString from "../../generic/NonLocalizedString.vue";

onMounted(async () => {
    getSectionValue();
});

const emit = defineEmits([OPEN_EDITOR, UPDATED]);

const schemeRight = ref<SchemeRights>();
const schemeRightStatement = ref<SchemeRightStatement[]>();
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
const editingStatement = ref<boolean>(false);

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
const currentSchemeRightStatement = computed(() => {
    return schemeRightStatement.value?.find(
        (tile) => tile.tileid === props.tileId,
    );
});

const metaStringLabel: MetaStringText = {
    deleteConfirm: $gettext("Are you sure you want to delete this label?"),
    language: $gettext("Statement Language"),
    name: $gettext("Statement"),
    type: $gettext("Statement Type"),
    noRecords: $gettext("No scheme right statement were found."),
};

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

function onUpdateSchemeRightReferenceDatatype(
    node: keyof SchemeRights,
    val: ControlledListItem[],
) {
    (schemeRight.value[node] as unknown) = val.map((item) => toRaw(item));
};

function onUpdateSchemeRightStatementReferenceDatatype(
    node: keyof SchemeRightStatement,
    val: ControlledListItem[],
) {
    (currentSchemeRightStatement.value[node] as unknown) = val.map((item) => toRaw(item));
};

function onUpdateString(node: keyof SchemeRightStatement, val: string) {
    (currentSchemeRightStatement.value[node] as unknown) = toRaw(val);
}

async function saveRights() {
    try {
        if (route.params.id === NEW) {
            const newSchemeInstance: SchemeInstance = {
                rights: [toRaw(schemeRight.value)],
            };
            const updated = await createScheme(newSchemeInstance);
            await router.push({
                name: "scheme",
                params: { id: updated.resourceinstanceid },
            });
        } else if (!schemeRight.value.tileid) {
            await createSchemeRights(route.params.id as string, schemeRight?.value);
        } else {
            await updateSchemeRights(
                route.params.id as string,
                schemeRight.value.tileid as string,
                schemeRight.value as SchemeRights,
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
    try {
        if (!currentSchemeRightStatement.value?.tileid) {
            await createSchemeRightStatement(route.params.id as string, currentSchemeRightStatement.value);
        } else {
            await updateSchemeRightStatement(
                route.params.id as string,
                currentSchemeRightStatement.value.tileid as string,
                currentSchemeRightStatement.value as SchemeRightStatement,
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
    const actorOptions = await getActorOptions();
    const schemeInstance = await fetchSchemeRights(route.params.id as string);
    if (schemeInstance?.right_statement && !Array.isArray(schemeInstance?.right_statement)) {
        schemeInstance.right_statement = [schemeInstance.right_statement];
    }
    schemeRight.value = schemeInstance?.rights;
    schemeRightStatement.value = schemeInstance?.right_statement;
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
    languageOptions.value = await getControlledListOptions(LANGUAGE_CONTROLLED_LIST);
    noteOptions.value = await getControlledListOptions(NOTE_CONTROLLED_LIST);
    metatypesOptions.value = await getControlledListOptions(METATYPES_CONTROLLED_LIST);
};

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
};

function editStatementValue(tileId: string) {
    editingStatement.value = true;
    const currentSchemeRightStatement = schemeRightStatement.value?.find(
        (tile) => tile.tileid === tileId,
    );

    if (currentSchemeRightStatement && currentSchemeRightStatement?.tileid === tileId) {
        emit(OPEN_EDITOR, currentSchemeRightStatement?.tileid);
    } else {
        toast.add({
            severity: ERROR,
            summary: $gettext("Error"),
            detail: $gettext("Could not find the selected statement to edit"),
        });
    }
};

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
                    :value="schemeRight?.right_holder"
                    :mode=VIEW
                />
                <h4>{{ $gettext('Rights Type') }}</h4>
                <ReferenceDatatype
                    :value="schemeRight?.right_type"
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
            <div v-if="!editingStatement">
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
                    @update="(val) => onUpdateSchemeRightReferenceDatatype('right_type', val)"
                />
                <Button
                    :label="$gettext('Update')"
                    @click="saveRights"
                ></Button>
            </div>
            <div v-if="!editingStatement">
                <h4>{{ $gettext('Statement') }}</h4>
                <NonLocalizedString
                    :value="currentSchemeRightStatement?.right_statement_content"
                    :mode="EDIT"
                    @update="
                        (val) =>
                            onUpdateString('right_statement_content', val)
                    "
                />
                <h4>{{ $gettext('Statement Language') }}</h4>
                <ReferenceDatatype
                    :value="currentSchemeRightStatement?.right_statement_language"
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
                    :value="currentSchemeRightStatement?.right_statement_type"
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
                    :value="currentSchemeRightStatement?.right_statement_type_metatype"
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
