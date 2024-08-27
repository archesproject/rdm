<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps({
  foo: {
    type: Object,
    required: true
  },
})

</script>

<template>
    <div 
        :class="{ 
            'is-even': foo.index % 2 === 0,
        }"
        style="width: 100%; padding: 1rem;"
    >
        <!-- {{ console.log(foo, this) }} -->
        <div>{{ foo.option.labels.find(bar => bar.language === 'en')['value'] }}</div>
    </div>
</template>

<style scoped>
.is-even {
    background-color: lightblue;
}
</style>