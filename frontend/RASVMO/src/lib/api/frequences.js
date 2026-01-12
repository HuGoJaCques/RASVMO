import { apiFetchGet } from "./client";

export function getFrequences() {
    return apiFetchGet('/frequences');
}