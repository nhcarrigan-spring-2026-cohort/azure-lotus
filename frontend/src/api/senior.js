import api from '../lib/axios.js';

/**
 * @param {string} caregiverId - The UUID of the caregiver.
 * @param {number} whichDay- The 'n' parameter for how many days back!
*/


const getCaregiverSeniorsList = async ({ caregiverId, whichDay = 0}) => {
  try {
    const { data } = await api.get(`/check_in/${caregiverId}/dashboard`, {
      params: {
        n: whichDay
      }
    });
    return data;
  } catch (error) {
    throw error.response;
  }
}; 

// get all the seniors a person is assigned to
export const getSeniorsByUser = async (caregiverId, whichDay) => {
  return await getCaregiverSeniorsList({ caregiverId, whichDay });
};
