<script lang="ts">
const MAXIMIZE = "maximize";
const SIDE = "side";
const CLOSE = "close";
</script>
<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import Button from "primevue/button";

const { $gettext } = useGettext();

const props = defineProps<{
    editorMax: boolean;
}>();

const emit = defineEmits([MAXIMIZE, SIDE, CLOSE]);

const toggleSize = () => {
    if (props.editorMax) {
        emit(MAXIMIZE);
    } else {
        emit(SIDE);
    }
};
</script>

<template>
    <div class="header">
        <div>
            <h2>{{ $gettext("Scheme Editor Tools") }}</h2>
            <div>
                <Button @click="toggleSize">
                    <i
                        :class="{
                            pi: true,
                            'pi-window-maximize': props.editorMax,
                            'pi-window-minimize': !props.editorMax,
                        }"
                        aria-hidden="true"
                    />
                </Button>
                <Button @click="$emit(CLOSE)">
                    <i
                        class="pi pi-times"
                        aria-hidden="true"
                    />
                </Button>
            </div>
        </div>
    </div>
</template>
<style scoped>
.header {
    background-color: #ddd;
}
.header div {
    margin: 0 1rem;
    display: flex;
    align-items: center;
}
.header div h2 {
    flex: 1;
}
</style>
