

import Card from './ui/Card';
import './DashboardCards.css';
import { useQuery } from '@tanstack/react-query';
import { getSeniorsByUser } from '../api/senior.js';
import { useAuthContext } from '../context/AuthContext';
import api from '../lib/axios.js';
// fetch today's checkin status for a single senior
const getSeniorDailyCheckin = async (seniorId) => {
  try {
    const res = await api.get(`/check_in/${seniorId}/daily`);
    return res.data?.data;  // { id, senior_id, status, checkin_time, ... }
  } catch (e) {
    if (e.response?.status === 404) return null;  // no checkin today = OK
    throw e;
  }
};
export default function DashboardCards({ date }) {
  const { user, accessToken } = useAuthContext();
  const caregiverId = user?.id;

  // Query 1 — get all monitored seniors
  const seniorsQuery = useQuery({
    queryKey: ['seniors', caregiverId, date],
    queryFn: () => getSeniorsByUser(caregiverId, date),
    enabled: !!caregiverId && !!accessToken,
  });

  const seniors = seniorsQuery.data?.data ?? [];

  // Query 2 — get today's checkin status for each senior
  // only runs after Query 1 succeeds
  const statusQuery = useQuery({
    queryKey: ['seniorDailyStatuses', seniors.map(s => s.senior_id), date],
    queryFn: async () => {
      const results = await Promise.all(
        seniors.map(async (senior) => {
          const checkin = await getSeniorDailyCheckin(senior.senior_id);
          return {
            ...senior,
            status: checkin?.status ?? 'no checkin',
            senior_time: checkin?.checkin_time ?? checkin?.completed_at ?? null,
          };
        })
      );
      return results;
    },
    enabled: seniors.length > 0,  // wait for seniors to load first
  });

  // loading + error states
  if (seniorsQuery.isPending) return <p>Loading seniors...</p>;
  if (seniorsQuery.isError)   return <p>Failed to load seniors.</p>;
  if (statusQuery.isPending)  return <p>Loading check-in statuses...</p>;
  if (statusQuery.isError)    return <p>Failed to load statuses.</p>;

  const seniorsWithStatus = statusQuery.data ?? [];

  // no seniors connected
  if (seniorsWithStatus.length === 0) {
    return (
      <div className="cards-board">
        <p>No seniors found.</p>
      </div>
    );
  }

  return (
    <div className="cards-board">
      {seniorsWithStatus.map((senior, index) => (
        <Card
          key={senior.relationship_id || index}
          senior_first_name={senior.first_name}
          senior_last_name={senior.last_name}
          senior_phone={senior.phone_number}
          status={senior.status}
          senior_time={senior.senior_time}
        />
      ))}
    </div>
  );
}