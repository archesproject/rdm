<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import Button from "primevue/button";

const { $gettext } = useGettext();
const props = defineProps<{
    titleText: string;
}>();

const buttonText = $gettext(`Add ${props.titleText}`);
</script>

<template>
    <div class="section">
        <div class="header">
            <h2>{{ props.titleText }}</h2>
            <div>
                <Button
                    :label="buttonText"
                    @click="$emit('openEditor')"
                ></Button>
            </div>
        </div>
        <div class="content">
            <slot></slot>
        </div>
    </div>
</template>

<style scoped>
.section {
    margin: 0 1rem;
}
.section .header {
    display: flex;
    align-items: center;
    border-bottom: 1px solid #ddd;
}
.section .header h2 {
    flex: 1;
}
.content {
    margin: 1rem 0;
}
</style>
