import {useMutation, useQuery} from '@tanstack/react-query';
import {
    getTodayCheckIn
} from '../../../api/checkin.js';

import CheckIn from '../../../components/checkin/CheckIn.jsx'
import {useAuthContext} from "../../../context/AuthContext.jsx";


export default function HomeSenior() {
    const {user} = useAuthContext();

    const todayCheckin = useQuery({
        queryKey: ['checkin'],
        queryFn: getTodayCheckIn,
        retry: 1,
    })

    if (todayCheckin.pending || !todayCheckin.data) return <div>Loading...</div>
    if (todayCheckin.isError) return <div>Failed to load check-in.</div>;

    const status = todayCheckin.data.data.status

    return (
        <>
            <div>Welcome {user?.email}</div>
            {
                status === "pending"
                    ? <CheckIn/>
                    : status === "completed"
                        ? <div>You have already checked In today</div>
                        : <div>You don't have a check in scheduled</div>
            }
        </>
    )

}