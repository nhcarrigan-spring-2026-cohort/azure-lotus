import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import SeniorCard from './SeniorCard';
import { getSeniorsByUser, addRelationship } from '../../api/senior.js';
import { useAuthContext } from '../../context/AuthContext.jsx';

export default function SeniorList() {
  const { user, accessToken } = useAuthContext();
  const queryClient = useQueryClient();

  // form state
  const [seniorEmail, setSeniorEmail] = useState('');
  const [showForm, setShowForm] = useState(false);

  // fetch existing relationships
  const { data, status } = useQuery({
    queryKey: ['seniors'],
    queryFn: () => getSeniorsByUser(user?.id, 0),
    enabled: !!user?.id && !!accessToken,
  });

  // add new relationship
  const addRelationshipMutation = useMutation({
    mutationFn: (email) => addRelationship({ email: email }),
    onSuccess: () => {
      queryClient.invalidateQueries(['seniors'])  // refresh list
      setSeniorEmail('')                          // clear input
      setShowForm(false)                          // hide form
      alert('Connection added successfully!')
    },
    onError: (error) => {
      alert(`Failed to add connection: ${error?.data?.detail || 'Unknown error'}`)
    }
  });

  const handleSubmit = () => {
    if (!seniorEmail) return alert('Please enter an email')
    addRelationshipMutation.mutate(seniorEmail)
  }

  if (status === 'pending') return <div>Loading...</div>
  if (status === 'error') return <div>Failed to load seniors.</div>

  const seniors =data?.data ?? []

  return (
    <div>
      <h3>Your Connections</h3>

      {/* existing seniors list */}
      {seniors.length === 0 ? (
        <p>No connections yet. Add one below!</p>
      ) : (
        seniors.map((senior) => (
          <SeniorCard key={senior.relationship_id} senior={senior} />
        ))
      )}

      {/* add connection form */}
      {showForm ? (
        <div>
          <input
            type="email"
            placeholder="Enter senior's email"
            value={seniorEmail}
            onChange={(e) => setSeniorEmail(e.target.value)}
          />
          <button
            onClick={handleSubmit}
            disabled={addRelationshipMutation.isPending}
          >
            {addRelationshipMutation.isPending ? 'Adding...' : 'Confirm'}
          </button>
          <button onClick={() => setShowForm(false)}>
            Cancel
          </button>
        </div>
      ) : (
        <button onClick={() => setShowForm(true)}>
          + Add Connection
        </button>
      )}
    </div>
  );
}