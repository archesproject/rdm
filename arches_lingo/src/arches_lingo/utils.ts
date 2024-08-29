import type { TreeNode } from "primevue/treenode";
import type { Labellable, Scheme } from "@/arches_lingo/types";

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
