import { API_BASE_URL } from "../config";

// GET
export async function apiFetchGet(endpoint){
    const response = await fetch(`${API_BASE_URL}${endpoint}`,{
        method : 'GET'
    });        
    if (!response.ok){
        throw new Error('Erreur API');
    }
    return response.json();
}

// POST
export async function apiFetchPost(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API ERROR ${response.status}: ${errorText}`);
    }        
    return response.json();
}
