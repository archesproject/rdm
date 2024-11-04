<script setup lang="ts">
import Button from "primevue/button";
const { section } = defineProps<{
    section: object;
    resourceKey: string | number;
}>();
</script>

<template>
    <div style="margin: 0 20px">
        <div
            style="
                display: flex;
                align-items: center;
                border-bottom: 1px solid #ddd;
            "
        >
            <h2>{{ resourceKey }}</h2>
            <div style="flex: 1"></div>
            <div><Button :label="resourceKey"> </Button></div>
        </div>
        <pre style="margin: 10px 0">
           {{ section }}
        </pre>
    </div>
</template>
