<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import SchemeReportSection from "@/arches_lingo/components/scheme/report/SchemeSection.vue";
const { $gettext } = useGettext();
</script>

<template>
    <SchemeReportSection :title-text="$gettext('Scheme URI')">
        todo
    </SchemeReportSection>
</template>
