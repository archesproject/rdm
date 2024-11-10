<script setup lang="ts">
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import SchemeLicense from "@/arches_lingo/components/scheme/report/SchemeLicense.vue";
import SchemeNote from "@/arches_lingo/components/scheme/report/SchemeNote.vue";
import SchemeUri from "@/arches_lingo/components/scheme/report/SchemeUri.vue";
import SchemeStandard from "@/arches_lingo/components/scheme/report/SchemeStandard.vue";
import SchemeAuthority from "@/arches_lingo/components/scheme/report/SchemeAuthority.vue";
</script>

<template>
    <div>
        <Splitter>
            <SplitterPanel>
                <SchemeNote />
                <SchemeAuthority />
                <SchemeStandard />
                <SchemeLicense />
                <SchemeUri />
            </SplitterPanel>
        </Splitter>
    </div>
</template>
