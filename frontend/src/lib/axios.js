import axios from 'axios';

let accessToken = null;

export const setAxiosAccessToken = (token) => {
  accessToken = token;
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASEURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

const refreshTokenApi = axios.create({
  baseURL: import.meta.env.VITE_API_BASEURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  }
})

// if there's an access token, attach it to the request
api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

// if access token expired (server returns 401), get a new access token and retry the request

api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config

      if(error?.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
          const refreshRes = await refreshTokenApi.post('/auth/refresh')
          const newAccessToken = refreshRes?.data?.access_token

          if(newAccessToken) {
            setAxiosAccessToken(newAccessToken)
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
          }

          return api(originalRequest)
        } catch (error) {
          return Promise.reject(error)
        }
      }

      return Promise.reject(error)
    }
)



export default api;
