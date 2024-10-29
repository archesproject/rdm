import type { Ref } from "vue";

import type { Label } from "@/arches_vue_utils/types";

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
    parents: {
        id: string;
        labels: Label[];
    }[];
    polyhierarchical: boolean;
}
