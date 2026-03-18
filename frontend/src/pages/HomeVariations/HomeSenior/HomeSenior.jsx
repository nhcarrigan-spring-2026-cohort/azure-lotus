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
    <>
      <div>Welcome {user?.email}</div>
      
      {status === 'pending'
        ? <CheckIn checkinId={checkinId} />         // shows "I'm OK" + "Alert Family"
        : status === 'completed'
          ? (
          <div>
          <div>You have already checked in today</div>
          <Button onClick={() => navigate('/dashboard')}>
              Go to Dashboard
            </Button>
          </div>
          )
          
          : (
            // no checkin exists → let user create one
            <div>
              <p>No check-in scheduled for today.</p>
              <Button
                onClick={() => createCheckin.mutate()}
                disabled={createCheckin.isPending}
              >
                {createCheckin.isPending ? 'Creating...' : 'Start Check-in'}
              </Button>
            </div>
          )
      }
    </>
  )
}