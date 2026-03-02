import {useMutation, useQuery} from '@tanstack/react-query';
import {
    getTodayCheckIn
} from '../../../api/checkin.js';

import CheckIn from '../../../components/checkin/CheckIn.jsx'


export default function HomeSenior() {
    const todayCheckin = useQuery({
        queryKey: ['checkin'],
        queryFn: getTodayCheckIn,
    })

    if (todayCheckin.pending) return <div>Loading...</div>


    return <>
        <div>{JSON.stringify(todayCheckin.data.data.status)}</div>
        <CheckIn/>
    </>
}