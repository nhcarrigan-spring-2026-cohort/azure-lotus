import { useQuery } from '@tanstack/react-query';
import SeniorCard from './SeniorCard';
import { getSeniorsByUser } from '../../api/senior.js';

export default function SeniorList() {
  const { data, status } = useQuery({
    queryKey: 'seniors',
    queryFn: getSeniorsByUser,
    // refetchOnMount: 'always',
    // refetchOnWindowFocus: 'always'
  });

  if (status === 'pending') return 'Loading...';

  return (
    <div>
      {data.map((senior) => (
        <SeniorCard senior={senior} />
      ))}
    </div>
  );
}
