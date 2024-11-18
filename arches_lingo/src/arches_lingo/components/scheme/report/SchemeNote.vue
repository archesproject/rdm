<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";

const save = () => {
    console.log("save");
};
const getSectionValue = async () => {
    console.log("update");
};

defineExpose({ save, getSectionValue });
const { $gettext } = useGettext();
</script>

<template>
    <SchemeReportSection :title-text="$gettext('Scheme Notes')">
        abc
    </SchemeReportSection>
</template>
