<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
const { $gettext } = useGettext();

const getSectionValue = async () => {
    console.log("update");
};
defineExpose({ getSectionValue });
</script>

<template>
    <SchemeReportSection :title-text="$gettext('Trusted Authorities')">
        todo
    </SchemeReportSection>
</template>
