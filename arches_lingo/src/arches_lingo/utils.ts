import type { Labellable } from "@/arches_lingo/types";

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
