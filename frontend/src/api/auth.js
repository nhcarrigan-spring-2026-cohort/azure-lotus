import axios from "axios";

export const api = axios.create({
    baseURL: import.meta.env.BASE_URL // TODO: might need to use VITE_BASE_URL? ALso rename it to API_BASEURL
})