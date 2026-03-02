import api from '../lib/axios.js';

// checkin, set status to completed
// Assuming a checkin would already be created with a "pending" status
export const completeCheckInMutation = async (checkinId) => {
  try {
    const res = await api.put(`/check_in/${checkinId}/complete`);
    return res.data;
  } catch (e) {
    throw e.response;
  }
};

// need help, set status to "alert"
// Assuming a checkin would already be created with a "pending" status
export const alertCheckInMutation = async (checkinId) => {
  try {
    const res = await api.put(`/check_in/${checkinId}/alert`);
    return res.data;
  } catch (e) {
    throw e.response;
  }
};

export const getTodayCheckIn = async () => {
  try {
    const response = await api.get('/check_in/today');
    return response.data;
  } catch (e) {
    throw e.response;
  }
}
