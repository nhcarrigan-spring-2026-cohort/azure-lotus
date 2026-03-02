import { useAuthContext } from '../../context/AuthContext.jsx';
import CheckInButton from '../ui/CheckInButton.jsx';
import styles from './CheckIn.module.css';
import { FaCheckCircle } from 'react-icons/fa';
import { FaPlus } from 'react-icons/fa';
import {useMutation, useQuery} from '@tanstack/react-query';
import {queryClient} from '../../lib/query-client.js';
import {
  completeCheckInMutation,
  alertCheckInMutation,
  getTodayCheckIn
} from '../../api/checkin.js';

export default function CheckIn({
  checkinId
}) {

  const completeCheckIn = useMutation({
    mutationFn: completeCheckInMutation,
    onSuccess: (data) => {
      alert(`Check In Successful. checkinId: ${JSON.stringify(data)}`);
      queryClient.invalidateQueries(['checkin']);
    },
    onError: (error) => {
      alert(`Check In Failed: ${error.message}`);
    },
  });

  const alertCheckIn = useMutation({
    mutationFn: alertCheckInMutation,
    onSuccess: () => {
      alert('Alert Successful');
      queryClient.invalidateQueries(['checkin']);
    },
    onError: (error) => {
      alert(`Alert Failed: ${error.message}`);
    },
  });

  return (
    <div className={styles.container}>
      <div>{`checkinId: ${checkinId}`}</div>
      <div className={styles.buttons}>
        <CheckInButton
          Icon={FaCheckCircle}
          text="I'm OK"
          subText="Check In"
          disabled={completeCheckIn.isPending}
            onClick={() => completeCheckIn.mutate(checkinId)}
        />
        <CheckInButton
          variant="danger"
          Icon={FaPlus}
          text="Alert Family"
          subText="Need Help!"
          disabled={alertCheckIn.isPending}
            onClick={() => alertCheckIn.mutate(checkinId)}
        />
      </div>
    </div>
  );
}
