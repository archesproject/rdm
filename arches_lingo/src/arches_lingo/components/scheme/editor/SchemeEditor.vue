<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import Button from "primevue/button";

import Tabs from "primevue/tabs";
import TabList from "primevue/tablist";
import Tab from "primevue/tab";
import TabPanels from "primevue/tabpanels";
import TabPanel from "primevue/tabpanel";
import SchemeNamespace from "../report/SchemeNamespace.vue";
import { onBeforeUpdate, onUpdated, ref } from "vue";
import type { DataComponentMode } from "@/arches_lingo/types";

const { $gettext } = useGettext();

const props = defineProps<{
    editorMax: boolean;
    activeTab: string;
}>();
type sectionTypes = typeof SchemeNamespace;
const childRefs = ref<Array<sectionTypes>>([]);
const editMode: DataComponentMode = "edit";
const schemeComponents = [
    {
        component: SchemeNamespace,
        props: {
            mode: editMode,
        },
        on: {
            update: onUpdated,
        },
        id: "namespace",
        editorTabName: $gettext("Scheme Namespace"),
    },
];

const emit = defineEmits(["maximize", "side", "close", "updated"]);


const toggleSize = () => {
    if (props.editorMax) {
        emit("maximize");
    } else {
        emit("side");
    }
};

schemeComponents.map((x) => {
    x.props.mode = "edit";
});

const getRef = (el: object | null, index: number) => {
    if (el != null) childRefs.value[index] = el as sectionTypes;
};

onBeforeUpdate(() => {
    childRefs.value = [];
});

const updateScheme = async () => {
    await Promise.all(
        childRefs.value.map(async (ref) => {
            return ref.save();
        }),
    );

    emit('updated');
};

</script>

<template>
    <div>
        <div class="header">
            <div>
                <h3>{{ $gettext("Editor Tools") }}</h3>
                <div>
                    <Button
                        :aria-label="$gettext('toggle editor size')"
                        @click="toggleSize"
                    >
                        <i
                            :class="{
                                pi: true,
                                'pi-window-maximize': props.editorMax,
                                'pi-window-minimize': !props.editorMax,
                            }"
                            aria-hidden="true"
                        />
                    </Button>
                    <Button
                        :aria-label="$gettext('close editor')"
                        @click="$emit('close')"
                    >
                        <i
                            class="pi pi-times"
                            aria-hidden="true"
                        />
                    </Button>
                </div>
            </div>
        </div>
        <div class="content">
            <Tabs :value="activeTab">
                <TabList>
                    <template
                        v-for="component in schemeComponents"
                        :key="component.id"
                    >
                        <Tab :value="component.id">{{
                            component.editorTabName
                        }}</Tab>
                    </template>
                </TabList>
                <TabPanels>
                    <template
                        v-for="(component, index) in schemeComponents"
                        :key="component.id"
                    >
                        <TabPanel :value="component.id">
                            <component
                                :is="component.component"
                                v-bind="component.props"
                                :ref="(el) => getRef(el, index)"
                                v-on="component.on"
                            />
                        </TabPanel>
                    </template>
                </TabPanels>
            </Tabs>
            <Button
                :label="$gettext('Update')"
                @click="updateScheme"
            ></Button>
        </div>
    </div>
</template>
<style scoped>
.header {
    background-color: var(--p-surface-200);
}
.header div {
    margin: 0 1rem;
    display: flex;
    align-items: center;
}
.header div h2 {
    flex: 1;
}
</style>
