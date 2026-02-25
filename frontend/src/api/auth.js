import api from '../lib/axios.js';

export const loginRequest = async ({ email, password }) => {
  try {
    const { data } = await api.post('/auth/login', {
      email,
      password,
    });
    return data;
  } catch (error) {
    throw error.response;
  }
};

/**
 * Register: auth/register
 * @param {string} firstname
 * @param {string} lastname
 * @param {string} email
 * @param {string} phoneNumber
 * @param {string} password
 * @returns {Promise<Object>}
 */

export const registerRequest = async ({
  firstname,
  lastname,
  email,
  phoneNumber,
  password,
}) => {
  try {
    const { data } = await api.post('/auth/register', {
      first_name: firstname,
      last_name: lastname,
      email,
      phone_number: phoneNumber,
      password,
    });
    return data;
  } catch (e) {
    throw e.response; // rethrow for react query to handle
  }
};
