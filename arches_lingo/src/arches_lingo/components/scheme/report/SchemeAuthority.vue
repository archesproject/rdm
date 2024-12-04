<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
const { $gettext } = useGettext();
const save = () => {
    console.log("save");
};
const getSectionValue = async () => {
    console.log("update");
};
defineExpose({ save, getSectionValue });
</script>

<template>
    <SchemeReportSection :title-text="$gettext('Trusted Authorities')">
        abc
    </SchemeReportSection>
</template>
