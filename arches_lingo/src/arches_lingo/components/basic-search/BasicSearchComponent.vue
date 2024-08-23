<script setup lang="ts">
import { ref, watch } from 'vue';
import { useGettext } from "vue3-gettext";

import AutoComplete from 'primevue/autocomplete';
import Button from "primevue/button";

const { $gettext } = useGettext();


const delay = 300;

const query = ref('');
const results = ref<Array<{ name: string; value: any }>[]>([]);
const isLoading = ref(false);
const shouldShowClearInputButton = ref(false);

const mockData = () => {
    return new Promise((resolve, _reject) => {
        setTimeout(() => {
            resolve([
                {
                    id: "d4e4db86-a948-4d6a-b89f-d1682d038afe",
                    labels: [
                        {
                            language: "de",
                            value: "Knochen",
                            valuetype: "prefLabel"
                        },
                        {
                            language: "pt",
                            value: "osso",
                            valuetype: "prefLabel"
                        },
                        {
                            language: "en",
                            value: "bone (material)",
                            valuetype: "prefLabel"
                        },
                        {
                            language: "fr",
                            value: "os",
                            valuetype: "prefLabel"
                        }
                    ],
                    parents: [
                        {
                            id: "b73e741b-46da-496c-8960-55cc1007bec4",
                            labels: [
                                {
                                    language: "en-US",
                                    value: "AAT Entries",
                                    valuetype: "prefLabel"
                                }
                            ]
                        },
                        {
                            id: "7764512c-494b-46e5-ad33-223836c8518b",
                            labels: [
                                {
                                    language: "en-US",
                                    value: "Materials",
                                    valuetype: "prefLabel"
                                }
                            ]
                        }
                    ],
                    polyhierarchical: false
                },
                {
                    id: "07dbe013-7dcf-4dd7-9df1-e72a9a855da5",
                    labels: [
                        {
                            language: "fr",
                            value: "bois",
                            valuetype: "prefLabel"
                        },
                        {
                            language: "en",
                            value: "wood (plant material)",
                            valuetype: "prefLabel"
                        }
                    ],
                    parents: [
                        {
                            id: "b73e741b-46da-496c-8960-55cc1007bec4",
                            labels: [
                                {
                                    language: "en-US",
                                    value: "AAT Entries",
                                    valuetype: "prefLabel"
                                }
                            ]
                        },
                        {
                            id: "7764512c-494b-46e5-ad33-223836c8518b",
                            labels: [
                                {
                                    language: "en-US",
                                    value: "Materials",
                                    valuetype: "prefLabel"
                                }
                            ]
                        }
                    ],
                    polyhierarchical: false
                }
            ]);
        }, 1000);
    });
};

const fetchData = async () => {
    shouldShowClearInputButton.value = false;

    if (!query.value) return;

    isLoading.value = true;
    try {
        const data = await mockData();
        results.value = data;
    } catch (error) {
        console.error('Error fetching data:', error);
        results.value = [];
    } finally {
        isLoading.value = false;
        shouldShowClearInputButton.value = true;
    }
};

const clearInput = () => {
  query.value = '';
  results.value = [];
  shouldShowClearInputButton.value = false;
};

</script>

<template>
    <div style="display: flex; align-items: center; position: relative;">
        <i 
            class="pi pi-search" 
            style="
                position: relative;
                left: 2rem;
                z-index: 1;
                font-weight: bold;
            "
        ></i>
        <AutoComplete 
            v-model="query" 
            :suggestions="results" 
            :placeholder="$gettext('Quick Search')"
            :delay="delay"
            @complete="fetchData" 
        >
            <template #option="slotProps">
                <div class="flex items-center">
                    {{ console.log(slotProps) }}
                    <div>{{ slotProps.option.id }}</div>
                </div>
            </template>
        </AutoComplete>
        <Button 
            v-if="shouldShowClearInputButton"
            @click="clearInput"
            class="p-button-text p-button-icon-only clear-button"
            style="
                position: absolute;
                right: 0.2rem;
                background-color: transparent;
                color: var(--p-input-color)
            "
        >
            <i
                class="pi pi-times" 
                aria-hidden="true"
            ></i>
        </Button>
    </div>
</template>

<style scoped>
.p-autocomplete {
    width: 100%;
}

:deep(.p-autocomplete-input) {
    width: 100%;
    text-indent: 2rem;
}
</style>