<script setup lang="ts">
const props = defineProps<{ value?: string | null }>();
</script>
<template>
    <p>{{ props.value }}</p>
</template>
