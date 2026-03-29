import api from '../lib/axios.js';

/**
 * @param {string} caregiverId - The UUID of the caregiver.
 * @param {number} whichDay- The 'n' parameter for how many days back!
*/


export const getCaregiverSeniorsList = async () => {
  try {
    const { data } = await api.get(`/relationships/monitors`);
    return data;
  } catch (error) {
    throw error.response;
  }
}; 
export const getSeniorsByUser = async (caregiverId, whichDay) => {
  try {
    const res = await api.get(`/relationships/monitoring?n=${whichDay}`);
    return res.data;  // returns { message: "...", data: [...] }
  } catch (e) {
    throw e.response;
  }
}
// get all the seniors a person is assigned to
//export const getSeniorsByUser = async (caregiverId, whichDay = 0) => {
  //return await getCaregiverSeniorsList({ caregiverId, whichDay });
//};

// add a new relationship (connect to a senior by email)
export const addRelationship = async (data) => {
  try {
    const res = await api.post('/relationships', data);
    return res.data;
  } catch (error) {
    throw error.response;
  }
};