import type { Concept, Labellable, Scheme } from "@/arches_lingo/types";

export const getItemLabel = (
    item: Concept,
    preferredLanguage: string,
): string | undefined => {
    const languageRoot = (language: string) => language.split(/[-_]/)[0];

    const findLabel = (language: string, valuetype: string) =>
        item.labels.find(
            (label) =>
                languageRoot(label.language) === language &&
                label.valuetype === valuetype,
        )?.value;

    let label = findLabel(preferredLanguage, "prefLabel");

    if (!label) label = findLabel(preferredLanguage, "altLabel");
    if (!label) label = findLabel(languageRoot(preferredLanguage), "prefLabel");
    if (!label) label = findLabel(languageRoot(preferredLanguage), "altLabel");
    if (!label)
        label = item.labels.find(
            (label) => label.valuetype === "prefLabel",
        )?.value;
    if (!label)
        label = item.labels.find(
            (label) => label.valuetype === "altLabel",
        )?.value;

    return label;
};

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
