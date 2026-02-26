import api from '../lib/axios.js'

// checkin, set status to completed
// Assuming a checkin would already be created with a "pending" status
export const completeCheckInMutation = async (checkinId ) => {
    try {
        // TODO: add checkin api call here to update checkin status
        return {
            checkinId,
            status: 'completed'
        };
    } catch (e) {
        throw e.response;
    }
}

// need help, set status to "alert"
// Assuming a checkin would already be created with a "pending" status
export const alertCheckInMutation = async (checkinId) => {
    try{
        // TODO: add api call to update checkin status
        return {
            checkinId,
            status: 'alert'
        }
    } catch (e) {
        throw e.response;
    }
}