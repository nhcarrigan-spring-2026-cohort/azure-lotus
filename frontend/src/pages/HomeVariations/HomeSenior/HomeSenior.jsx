import {useMutation, useQuery,useQueryClient} from '@tanstack/react-query';
import { useNavigate } from 'react-router';
import {
    getTodayCheckIn,createCheckIn 
} from '../../../api/checkin.js';

import CheckIn from '../../../components/checkin/CheckIn.jsx'
import {useAuthContext} from "../../../context/AuthContext.jsx";
import Button from '../../../components/ui/Button';

export default function HomeSenior() {
  const { user } = useAuthContext();
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  // fetch today's checkin
  const todayCheckin = useQuery({
    queryKey: ['checkin'],
    queryFn: getTodayCheckIn,
    retry: 1,
  });

  // create a new checkin if none exists
  const createCheckin = useMutation({
    mutationFn: createCheckIn,
    onSuccess: () => {
      queryClient.invalidateQueries(['checkin'])  // refetch after creating
    },
    onError: (error) => {
      alert(`Failed to create check-in: ${error?.data?.detail || 'Unknown error'}`)
    }
  });

  if (todayCheckin.isPending) return <div>Loading...</div>
  if (todayCheckin.isError) return <div>Failed to load check-in.</div>

  const status = todayCheckin.data?.data?.status
  const checkinId = todayCheckin.data?.data?.id
  
  return (
  <div className="homesenior-container">
    <p className="homesenior-welcome">Welcome, {user?.email}</p>

    <div className="homesenior-card">
      {status === 'pending' ? (
        <>
          <div className="homesenior-icon">👋</div>
          <h2 className="homesenior-title">How are you today?</h2>
          <CheckIn checkinId={checkinId} />
        </>
      ) : status === 'completed' ? (
        <div className="homesenior-completed">
          <div className="homesenior-icon">✅</div>
          <h2 className="homesenior-title">All Good!</h2>
          <p>You have already checked in today</p>
          <Button onClick={() => navigate('/dashboard')}>
            Go to Dashboard
          </Button>
        </div>
      ) : (
        <div className="homesenior-no-checkin">
          <div className="homesenior-icon">📋</div>
          <h2 className="homesenior-title">No check-in yet</h2>
          <p>No check-in scheduled for today.</p>
          <Button
            onClick={() => createCheckin.mutate()}
            disabled={createCheckin.isPending}
          >
            {createCheckin.isPending ? 'Creating...' : "Start Today's Check-in"}
          </Button>
        </div>
      )}
    </div>
  </div>
);
}