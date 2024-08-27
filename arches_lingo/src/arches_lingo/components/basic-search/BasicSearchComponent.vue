<script setup lang="ts">
import { nextTick, ref } from 'vue';
import { useGettext } from "vue3-gettext";

import AutoComplete from 'primevue/autocomplete';
import Button from "primevue/button";

import SortAndFilterControls from '@/arches_lingo/components/basic-search/SortAndFilterControls.vue';
import SearchResult from '@/arches_lingo/components/basic-search/SearchResult.vue';

const { $gettext } = useGettext();


const instance = ref(null);
const query = ref(null);
const queryString = ref('');
const results = ref([]);
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
                },
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
                },
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
                },
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
                },
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
                },
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
                },
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
                },
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
                },
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
                },
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
                },
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
                },
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
                },
            ]);
        }, 1000);
    });
};

const fetchData = async () => {
    isLoading.value = true;
    shouldShowClearInputButton.value = false;
    instance.value.overlayVisible = false;

    try {
        const data = await mockData();
        results.value = data;
        shouldShowClearInputButton.value = true;
    } catch (error) {
        console.error('Error fetching data:', error);
    } finally {
        isLoading.value = false;
    }
};

const clearInput = () => {
    query.value = '';
    shouldShowClearInputButton.value = false;
};

const updateQuery = () => {
    query.value = queryString.value;
};

const keepOverlayVisible = () => {
    if (query.value && results.value.length) {
        nextTick(() => instance.value?.show());
    }
};

const updateQueryString = (value: string | object) => {
    if (!value) {
        shouldShowClearInputButton.value = false;
    }

    if (typeof value === 'string') { 
        queryString.value = value;
    }
}

</script>

<template>
    <div style="display: flex; align-items: center; position: relative;">
        <i class="pi pi-search search-icon" />

        <AutoComplete 
            ref="instance"
            v-model="query" 
            :suggestions="results" 
            :placeholder="$gettext('Quick Search')"
            @complete="fetchData" 
            @option-select="updateQuery"
            @before-hide="keepOverlayVisible"
            @update:model-value="updateQueryString"
            :pt="{
                option: () => ({
                    style: {
                        padding: 0,
                    },
                }),
                overlay: () => ({
                    style: {
                        transform: 'translateY(2.3rem)',
                        maxHeight: '60vh'
                    }
                }),
            }"
        >
            <template #option="slotProps">
                <SearchResult :search-result="slotProps"/>
            </template>
        </AutoComplete>

        <Button 
            aria-label="Clear Input"
            v-if="shouldShowClearInputButton"
            @click="clearInput"
            class="p-button-text clear-button"
            style="background-color: transparent;"
            icon="pi pi-times"
        />
    </div>

    <SortAndFilterControls />
</template>

<style scoped>
.search-icon {
    position: absolute;
    inset-inline-start: 1rem;
    z-index: 1;
    font-weight: bold;
}

.clear-button {
    position: absolute;
    inset-inline-end: 0.2rem;
    color: var(--p-input-color);
}

.p-autocomplete {
    width: 100%;
}

:deep(.p-autocomplete .p-autocomplete-input) {
    width: 100%;
    padding-right: 2.5rem;
    padding-left: 2.5rem;
}
</style>