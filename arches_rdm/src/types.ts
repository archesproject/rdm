export type Concept = {
    id: string,
    labels: Label[],
    narrower: Concept[],
};

export type Scheme = {
    id: string,
    labels: Label[],
    top_concepts: Concept[],
};

export type Label = {
    value: string,
    language: string,
    valuetype: "prefLabel" | "altLabel" | "unknown",
};

export type Labellable = Concept | Scheme;
