<script setup lang="ts">
import { ref } from "vue";
import { useGettext } from "vue3-gettext";

import Button from "primevue/button";
import Dialog from "primevue/dialog";

import BasicSearchComponent from "@/arches_lingo/components/basic-search/BasicSearchComponent.vue";

const { $gettext } = useGettext();

const visible = ref(false);
</script>

<template>
    <Button
        icon="pi pi-search"
        :label="$gettext('Search')"
        @click="visible = true"
    />

    <Dialog
        v-model:visible="visible"
        :dismissable-mask="true"
        :modal="true"
        :close-on-escape="true"
        :show-header="false"
        :pt="{
            content: () => ({
                style: {
                    padding: 0,
                },
            }),
        }"
        style="margin-top: 6rem"
        position="top"
    >
        <div style="width: 80vw">
            <BasicSearchComponent
                :search-results-per-page="25"
                :search-result-item-size="38"
            />
        </div>
    </Dialog>
</template>

<style scoped></style>
