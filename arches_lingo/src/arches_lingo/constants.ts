import type { InjectionKey } from "vue";

import type { UserRefAndSetter } from "@/arches_lingo/types.ts";

export const ANONYMOUS = "anonymous";
export const ERROR = "error";
export const DEFAULT_ERROR_TOAST_LIFE = 8000;

export const userKey = Symbol() as InjectionKey<UserRefAndSetter>;
