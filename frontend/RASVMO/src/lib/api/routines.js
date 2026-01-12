import { apiFetchGet, apiFetchPost } from "./client";

export function getRoutinesFreq(frequence) {
    return apiFetchGet(`/routine/${frequence}`);
}

export function getRoutinesJour() {
    return apiFetchGet(`/get_routine_jour`);
}

export function addRoutines(data) {
    return apiFetchPost('/routine', data);
}