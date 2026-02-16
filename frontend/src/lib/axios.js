import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASEURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    // TODO set headers
  },
});

export default api;
