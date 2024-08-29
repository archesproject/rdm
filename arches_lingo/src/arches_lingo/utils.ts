import type { Language } from "@/arches/types";
import type { TreeNode } from "primevue/treenode";
import type {
    Concept,
    IconLabels,
    Labellable,
    NodeAndParentInstruction,
    Scheme,
} from "@/arches_lingo/types";

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

// Tree builder
export const treeFromSchemes = (
    schemes: Scheme[],
    selectedLanguage: Language,
    iconLabels: IconLabels,
    focusedNode: TreeNode | null,
) => {
    // Use a closure to avoid passing around params (selectedLanguage, etc).
    const conceptAsNodeAndInstruction = (
        concept: Concept,
    ): NodeAndParentInstruction => {
        return conceptOrSchemeAsNodeAndInstruction(concept, concept.narrower);
    };
    const schemeAsNodeAndInstruction = (
        scheme: Scheme,
    ): NodeAndParentInstruction => {
        return conceptOrSchemeAsNodeAndInstruction(scheme, scheme.top_concepts);
    };

    const conceptOrSchemeAsNodeAndInstruction = (
        labellable: Labellable,
        children: Concept[],
    ): NodeAndParentInstruction => {
        let childrenAsNodes: TreeNode[];
        const nodesAndInstructions = children.map((child) =>
            conceptAsNodeAndInstruction(child),
        );
        const parentOfFocusedNode = nodesAndInstructions.find(
            (obj) => obj.parentShouldHideSiblings,
        );
        if (parentOfFocusedNode) {
            childrenAsNodes = [parentOfFocusedNode.node];
        } else {
            childrenAsNodes = nodesAndInstructions.map((obj) => obj.node);
        }

        const node: TreeNode = {
            key: labellable.id,
            label: bestLabel(labellable, selectedLanguage.code).value,
            children: childrenAsNodes,
            data: labellable,
            iconLabel: dataIsScheme(labellable)
                ? iconLabels.scheme
                : iconLabels.concept,
        };
        let parentShouldHideSiblings = !!parentOfFocusedNode;
        if (!parentShouldHideSiblings) {
            const focalNodeIdx = node.children!.findIndex(
                (child: TreeNode) => child.data.id === focusedNode?.data?.id,
            );
            if (focalNodeIdx > -1) {
                node.children = [node.children![focalNodeIdx]];
                parentShouldHideSiblings = true;
            }
        }
        return { node, parentShouldHideSiblings };
    };

    const focalNodeIdx = schemes.findIndex(
        (scheme) => scheme.id === focusedNode?.data?.id,
    );
    if (focalNodeIdx > -1) {
        return [schemeAsNodeAndInstruction(schemes[focalNodeIdx]).node];
    }
    const nodesAndInstructions = schemes.map((scheme: Scheme) =>
        schemeAsNodeAndInstruction(scheme),
    );
    const parentOfFocusedNode = nodesAndInstructions.find(
        (obj) => obj.parentShouldHideSiblings,
    );
    if (parentOfFocusedNode) {
        return [parentOfFocusedNode.node];
    }
    return nodesAndInstructions.map((obj) => obj.node);
};
