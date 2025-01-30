<script setup lang="ts">
import { fetchResourceOptions } from "@/arches_lingo/api.ts";
import { onMounted, ref } from "vue";
// import Tabs from "primevue/tabs";
// import TabList from "primevue/tablist";
// import Tab from "primevue/tab";
// import TabPanels from "primevue/tabpanels";
// import TabPanel from "primevue/tabpanel";
//import ResourceInstanceRelationships from "./ResourceInstanceRelationships.vue";

const props = defineProps<{
    graphSlug: string;
}>();

// const emits = defineEmits(["update"]);
const tabs = ref({});
// const widgets = ref({
//     resourceInstanceRelationships: {
//         component: ResourceInstanceRelationships,
//     },
// });

onMounted(async () => {
    const options = await fetchResourceOptions(props.graphSlug);
    console.log(options.actions.POST);
    //for (const entry in options.actions.POST) {
    //const entryObj = options.actions.POST[entry];
    //const children = entryObj?.child?.children ?? entryObj?.children;
    // if (children) {
    //     for (const obj in children) {
    //         console.log(obj);
    //         if (children[obj]?.visible) {
    //             if (tabs.value[entry]) {
    //                 tabs.value[entry].children = [
    //                     children[obj],
    //                     ...tabs.value[entry].children,
    //                 ];
    //             } else {
    //                 tabs.value[entry] = {};
    //                 tabs.value[entry].key = entry;
    //                 tabs.value[entry].label = entryObj.label;
    //                 tabs.value[entry].children = [children[obj]];
    //             }
    //         }
    //     }
    // }
    //}
    console.log(tabs.value);
});
</script>

<template>
    <div style="min-width: 50vh; max-width: 75vh">
        <!-- <Tabs
            value="0"
            scrollable
        >
            <TabList>
                <template v-for="tab in tabs">
                    <Tab :value="tab.key">{{ tab.label }}</Tab>
                </template>
            </TabList>
            <TabPanels>
                <template v-for="tab in tabs">
                    <TabPanel :value="tab.key">
                        <div v-for="child in tab.children">
                            {{ child }}
                            <component :is="widgets[child.component]" :graph-slug="props.graphSlug" />
                        </div>
                    </TabPanel>
                </template>
            </TabPanels>
        </Tabs> -->
    </div>
</template>
