import api from '../lib/axios.js';

// get all the seniors a person is assigned to
export const getSeniorsByUser = async (userId) => {
  try {
    // const { data } = await api.get(`/relationship/${userId}/monitoring`)
    return [
      { firstname: 'Patrick', lastname: 'Smith', phoneNumber: '1234567890' },
      { firstname: 'John', lastname: 'Doe', phoneNumber: '0987654321' },
      { firstname: 'Jane', lastname: 'Doe', phoneNumber: '0987654321' },
    ];
  } catch (e) {
    throw e.response;
  }
};
