import type { Ref } from "vue";
import type { TreeNode } from "primevue/treenode";

export interface User {
    first_name: string;
    last_name: string;
    username: string;
}

// Prop injection types
export interface UserRefAndSetter {
    user: Ref<User | null>;
    setUser: (userToSet: User | null) => void;
}

export interface Concept {
    id: string;
    labels: Label[];
    narrower: Concept[];
}

export interface Scheme {
    id: string;
    labels: Label[];
    top_concepts: Concept[];
}

export interface Label {
    value: string;
    language: string;
    valuetype: "prefLabel" | "altLabel" | "unknown";
}

export type Labellable = Concept | Scheme;

export type RowSetter = (val: Labellable | null) => void;

export interface NodeAndParentInstruction {
    node: TreeNode;
    parentShouldHideSiblings: boolean;
}

export interface IconLabels {
    concept: string;
    scheme: string;
}
