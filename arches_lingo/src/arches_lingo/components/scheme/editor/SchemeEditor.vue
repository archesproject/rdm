<script setup lang="ts">
import { useGettext } from "vue3-gettext";
import Button from "primevue/button";

import { EDIT, MAXIMIZE, MINIMIZE, CLOSE } from "@/arches_lingo/constants.ts";

const { $gettext } = useGettext();
const props = defineProps<{
    isEditorMaximized: boolean;
    component: any;
    tileId?: string;
}>();

const emit = defineEmits([MAXIMIZE, MINIMIZE, CLOSE]);

function toggleSize() {
    if (props.isEditorMaximized) {
        emit(MINIMIZE);
    } else {
        emit(MAXIMIZE);
    }
}
</script>

<template>
    <div class="header">
        <div>
            <h3>{{ $gettext("Editor Tools") }}</h3>
            <div>
                <Button
                    :aria-label="$gettext('toggle editor size')"
                    @click="toggleSize"
                >
                    <i
                        :class="{
                            pi: true,
                            'pi-window-maximize': props.isEditorMaximized,
                            'pi-window-minimize': !props.isEditorMaximized,
                        }"
                        aria-hidden="true"
                    />
                </Button>
                <Button
                    :aria-label="$gettext('close editor')"
                    @click="$emit(CLOSE)"
                >
                    <i
                        class="pi pi-times"
                        aria-hidden="true"
                    />
                </Button>
            </div>
        </div>
    </div>
    <div class="content">
        <!-- <h3>{{ props.component.name }}</h3> -->

        <component
            :is="props.component"
            v-bind="{ mode: EDIT, tileId: props.tileId }"
        />
    </div>
</template>
<style scoped>
.header div {
    margin: 0 1rem;
    display: flex;
    align-items: center;
}
.header div h3 {
    flex: 1;
}
</style>
