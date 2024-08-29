import type { TreeNode } from "primevue/treenode";
import type { Labellable, Scheme } from "@/arches_lingo/types";

export const bestLabel = (item: Labellable, languageCode: string) => {
    const labelsInLang = item.labels.filter(
        (label) => label.language === languageCode,
    );
    const bestLabel =
        labelsInLang.find((value) => value.valuetype === "prefLabel") ??
        labelsInLang.find((value) => value.valuetype === "altLabel") ??
        labelsInLang.find((value) => value.valuetype === "prefLabel");
    if (!bestLabel) {
        return item.labels[0];
    }
    return bestLabel;
};

// Duck-typing helpers
export const dataIsScheme = (data: Labellable) => {
    return (data as Scheme).top_concepts !== undefined;
};
export const dataIsConcept = (data: Labellable) => {
    return !dataIsScheme(data);
};
export const nodeIsConcept = (node: TreeNode) => {
    return !nodeIsScheme(node);
};
export const nodeIsScheme = (node: TreeNode) => {
    return dataIsScheme(node.data);
};
