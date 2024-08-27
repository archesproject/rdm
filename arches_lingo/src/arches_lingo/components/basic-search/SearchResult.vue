<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps({
  foo: {
    type: Object,
    required: true
  },
})

const getItemLabel = item => item.labels.find(bar => bar.language === 'en')['value'];

const getParentLabels = item => {
    return item.parents
        .map(parent => {
            const enLabel = parent.labels.find(label => label.language === "en-US");
            return enLabel ? enLabel.value : "";
        })
        .join(" > ");
};

</script>

<template>
    <div 
        :class="{ 'is-even': foo.index % 2 === 0 }"
        style="width: 100%; padding: 0.5rem; display: flex;"
    >
        {{ console.log(foo) }}
        <i class="pi pi-paperclip" />

        <div style="margin: 0 0.5rem;">
            {{ getItemLabel(foo.option) }}
        </div>
        
        <div style="margin: 0 0.5rem;">
            {{ getParentLabels(foo.option) }}
        </div>
    </div>
</template>

<style scoped>
.is-even {
    background-color: lightblue;
}
</style>