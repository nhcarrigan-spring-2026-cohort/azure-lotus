import styles from './SeniorCard.module.css';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { removeRelationship } from '../../api/senior.js';


export default function SeniorCard({ senior }) {
  const queryClient = useQueryClient();

  const deleteMutation = useMutation({
    mutationFn: () => removeRelationship(senior.relationship_id),
    onSuccess: () => {
      queryClient.invalidateQueries(['seniors']);
    },
    onError: () => {
      alert('Failed to delete connection');
    }
  });

  return (
    <div className={styles.seniorCard}>
      <h2>{`${senior.first_name} ${senior.last_name}`}</h2>
      <p>Email: {senior.email}</p>
      <p>Phone number: {senior.phone_number}</p>
      <button
        onClick={() => deleteMutation.mutate()}
        disabled={deleteMutation.isPending}
      >
        {deleteMutation.isPending ? 'Deleting...' : 'Delete Connection'}
      </button>
    </div>
  );
}
