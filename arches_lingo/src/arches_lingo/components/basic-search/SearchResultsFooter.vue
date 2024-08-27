<script setup lang="ts">
import { defineEmits } from "vue";
import Paginator from "primevue/paginator";
import PageEvent from "primevue/paginator";

const emit = defineEmits(["page-change"]);

defineProps({
    searchResultsPerPage: {
        type: Number,
        required: true,
    },
    totalSearchResultsCount: {
        type: Number,
        required: true,
    },
});

const emitPageChangeEvent = (event: typeof PageEvent) => {
    emit("page-change", event);
};
</script>

<template>
    <Paginator
        :rows="searchResultsPerPage"
        :total-records="totalSearchResultsCount"
        style="position: sticky; bottom: 0"
        :always-show="false"
        @page="emitPageChangeEvent"
    />
</template>
