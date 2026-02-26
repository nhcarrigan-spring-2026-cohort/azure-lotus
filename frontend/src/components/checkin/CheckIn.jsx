import {useAuthContext} from "../../context/AuthContext.jsx";
import CheckInButton from '../ui/CheckInButton.jsx'
import styles from './CheckIn.module.css'
import {FaCheckCircle} from 'react-icons/fa'
import { FaPlus } from "react-icons/fa";
import { useMutation } from '@tanstack/react-query';
import { completeCheckInMutation, alertCheckInMutation } from '../../api/checkin.js';


export default function CheckIn() {
    const { user, isAuthenticated } = useAuthContext();

    const completeCheckIn = useMutation({
        mutationFn: completeCheckInMutation,
        onSuccess: () =>{
            alert('Check In Successful')
        },
        onError: (error) => {
            alert(`Check In Failed: ${error.message}`)
        }
    })

    const alertCheckIn = useMutation({
        mutationFn: alertCheckInMutation,
        onSuccess: () =>{
            alert('Alert Successful')
        },
        onError: (error) => {
            alert(`Alert Failed: ${error.message}`)
        }
    })

    return (
        <div className={styles.container}>
            <div>Welcome {user?.email}</div>
            <div className={styles.buttons}>
                <CheckInButton
                    Icon={FaCheckCircle}
                    text="I'm OK"
                    subText="Check In"
                    disabled={completeCheckIn.isPending}
                    onClick={() => completeCheckIn.mutate()}
                />
                <CheckInButton
                    variant="danger"
                    Icon={FaPlus}
                    text="Alert Family"
                    subText="Need Help!"
                    disabled={alertCheckIn.isPending}
                    onClick={() => alertCheckIn.mutate()}
                />
            </div>

        </div>

    )
}
