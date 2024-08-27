import type { InjectionKey } from "vue";

import type { UserRefAndSetter } from "@/arches_lingo/types.ts";

export const ANONYMOUS = "anonymous";
export const ERROR = "error";
export const DEFAULT_ERROR_TOAST_LIFE = 8000;

export const USER_KEY = Symbol() as InjectionKey<UserRefAndSetter>;

export const ENGLISH = {
    code: "en",
    default_direction: "ltr" as const,
    id: 1,
    isdefault: true,
    name: "English",
    scope: "system",
};
