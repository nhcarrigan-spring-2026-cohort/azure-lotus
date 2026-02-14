import axios from 'axios';

const api = axios.create({
  // baseURL: import.meta.env.API_BASEURL
  // withCredentials: true,
  baseURL: 'https://dummyjson.com/',
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json',
    // TODO set headers
  },
});

export default api;
