import { getItemLabel } from "@/arches_vue_utils/utils.ts";

import type { TreeNode } from "primevue/treenode";
import type { Language } from "@/arches_vue_utils/types";
import type {
    Concept,
    IconLabels,
    NodeAndParentInstruction,
    Scheme,
} from "@/arches_lingo/types";

// Duck-typing helpers
export function dataIsScheme(data: Concept | Scheme) {
    return (data as Scheme).top_concepts !== undefined;
}
export function dataIsConcept(data: Concept | Scheme) {
    return !dataIsScheme(data);
}

// Tree builder
export function treeFromSchemes(
    schemes: Scheme[],
    selectedLanguage: Language,
    systemLanguage: Language,
    iconLabels: IconLabels,
    focusedNode: TreeNode | null,
): TreeNode[] {
    function buildNode(
        item: Concept | Scheme,
        childNodes: TreeNode[],
    ): TreeNode {
        return {
            key: item.id,
            label: getItemLabel(
                item,
                selectedLanguage.code,
                systemLanguage.code,
            ).value,
            children: childNodes,
            data: item,
            iconLabel: dataIsScheme(item)
                ? iconLabels.scheme
                : iconLabels.concept,
        };
    }

    // When traversing the tree, notice whether the node is focused, and if so,
    // memoize/instruct that the parent should hide its siblings.
    function processItem(
        item: Concept | Scheme,
        children: Concept[],
    ): NodeAndParentInstruction {
        let childrenAsNodes: TreeNode[];
        const nodesAndInstructions = children.map((child) =>
            processItem(child, child.narrower),
        );
        const parentOfFocusedNode = nodesAndInstructions.find(
            (obj) => obj.shouldHideSiblings,
        );
        if (parentOfFocusedNode) {
            childrenAsNodes = [parentOfFocusedNode.node];
        } else {
            childrenAsNodes = nodesAndInstructions.map((obj) => obj.node);
        }

        const node: TreeNode = buildNode(item, childrenAsNodes);
        let shouldHideSiblings = !!parentOfFocusedNode;
        if (!shouldHideSiblings) {
            const focalNode = node.children!.find(
                (child: TreeNode) => child.data.id === focusedNode?.data?.id,
            );
            if (focalNode) {
                node.children = [focalNode];
                shouldHideSiblings = true;
            }
        }
        return { node, shouldHideSiblings };
    }

    // If this scheme is focused, immediately process and return it.
    const focalScheme = schemes.find((sch) => sch.id === focusedNode?.data?.id);
    if (focalScheme) {
        return [processItem(focalScheme, focalScheme.top_concepts).node];
    }

    // Otherwise, process schemes until a focused node is found.
    const reshapedSchemes = [];
    for (const scheme of schemes) {
        const { node, shouldHideSiblings } = processItem(
            scheme,
            scheme.top_concepts,
        );
        if (shouldHideSiblings) {
            return [node];
        } else {
            reshapedSchemes.push(node);
        }
    }

    return reshapedSchemes;
}
