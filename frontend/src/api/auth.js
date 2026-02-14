import api from '../lib/axios.js';

export const loginRequest = async ({ email, password }) => {
  const { data } = await api.post('/auth/login', {
    email,
    password,
  });
  return data;
};

/**
 * Register: auth/register
 * @param {string} firstname
 * @param {string} lastname
 * @param {string} email
 * @param {string} phoneNumber
 * @param {string} password
 * @typedef {"family" | "volunteer" | "senior"} UserRole
 * @returns {Promise<Object>}
 */

export const registerRequest = async ({
  firstname,
  lastname,
  email,
  phoneNumber,
  password,
  role,
}) => {
  try {
    const { data } = await api.post('/auth/register', {
      first_name: firstname,
      last_name: lastname,
      email,
      phone_number: phoneNumber,
      password,
      roles: role,
    });
    return data;
  } catch (e) {
    // TODO: Backend should return more specific error messages
    throw e; // rethrow for react query to handle
  }
};
