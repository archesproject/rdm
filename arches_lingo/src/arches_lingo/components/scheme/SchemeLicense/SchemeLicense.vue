<script setup lang="ts">
import { inject, onMounted, ref, type Ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useGettext } from "vue3-gettext";
import { useToast } from "primevue/usetoast";
import {
    fetchLingoResource,
    fetchLingoResources,
} from "@/arches_lingo/api.ts";
import { fetchLists } from "@/arches_controlled_lists/api.ts";

import type {
    ControlledListResult,
    ControlledListItemResult,
    DataComponentMode,
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
} from "@/arches_lingo/constants.ts";
import type { Language } from "@/arches_vue_utils/types.ts";
import SchemeLicenseViewer from "@/arches_lingo/components/scheme/SchemeLicense/components/SchemeLicenseViewer.vue";
import SchemeLicenseEditor from "@/arches_lingo/components/scheme/SchemeLicense/components/SchemeLicenseEditor.vue";

const props = defineProps<{
    mode: DataComponentMode;
    tileId?: string | null;
    graphSlug: string;
    nodeGroupAlias: string;
    resourceInstanceId: string | undefined;
}>();

const isLoading = ref(false);
const schemeRights = ref<SchemeRights>({});
const schemeRightStatement = ref<SchemeRightStatement>({});
const shouldCreateNewTile = Boolean(props.mode === EDIT && !props.tileId);

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

const referenceNodeConfig = [
    {
        nodeAlias: "right_type",
        listRef: rightTypeOptions,
        listName: "Right Types",
    },
    {
        nodeAlias: "right_statement_language",
        listRef: languageOptions,
        listName: "Languages",
    },
    {
        nodeAlias: "right_statement_type",
        listRef: noteOptions,
        listName: "note",
    },
    {
        nodeAlias: "right_statement_type_metatype",
        listRef: metatypesOptions,
        listName: "Metatypes",
    },
];

async function getActorOptions() {
    const options_person = await fetchLingoResources("person");
    const options_group = await fetchLingoResources("group");
    const options = options_person.concat(options_group);

    actorRdmOptions.value = options.map((option: ResourceInstanceResult) => {
        const result: ResourceInstanceReference = {
            display_value: option.descriptors[selectedLanguage.value.code].name,
            resourceId: option.resourceinstanceid,
            ontologyProperty: "",
            inverseOntologyProperty: "",
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
        const options: ControlledListItem[] = [];
        matchingList.items.forEach((item: ControlledListItemResult) => {
            options.push({
                uri: item.uri,
                list_id: item.list_id,
                labels: item.values,
            });
            if (item.children) {
                item.children.forEach((child) => {
                    const indentation = "- ";
                    child.values.map((value) => {
                        value.value =
                            indentation.repeat(child.depth) + value.value;
                    });
                    options.push({
                        uri: child.uri,
                        list_id: child.list_id,
                        labels: child.values,
                    });
                });
            }
        });
        node.listRef.value = options;
    });
}

async function getSectionValue() {
    if (route.params.id === NEW) {
        return;
    }
    const schemeInstance = await fetchLingoResource(
        "scheme",
        route.params.id as string,
    );
    schemeRights.value = schemeInstance?.rights ?? {};
    if (schemeInstance?.rights) {
        parentExists.value = true;
    }
    schemeRightStatement.value = schemeInstance?.rights?.right_statement ?? {};
}

defineExpose({ getSectionValue });
</script>

<template>
    <ProgressSpinner
        v-if="isLoading"
        style="width: 100%"
    />
    <template v-else>
        <SchemeLicenseViewer
            v-if="mode === VIEW"
            :scheme-rights="schemeRights"
            :scheme-right-statement="schemeRightStatement"
        />
        <SchemeLicenseEditor
            v-else-if="mode === EDIT"
            :scheme-rights="shouldCreateNewTile ? undefined : schemeRights"
            :scheme-right-statement="shouldCreateNewTile ? undefined : schemeRightStatement"
        />
    </template>
</template>
