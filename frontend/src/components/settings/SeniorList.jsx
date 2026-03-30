import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import SeniorCard from './SeniorCard';
import { getSeniorsByUser, addRelationship, getCaregiverSeniorsList } from '../../api/senior.js';
import { useAuthContext } from '../../context/AuthContext.jsx';
import Button from '../ui/Button';

export default function SeniorList() {
  const { user, accessToken } = useAuthContext();
  const queryClient = useQueryClient();

  // form state
  const [seniorEmail, setSeniorEmail] = useState('');
  const [showForm, setShowForm] = useState(false);
  
  // Query to fetch seniors for the logged-in users
  const { data, status } = useQuery({
  queryKey: ['seniors', user?.id],
  queryFn: async () => {
    const results = await Promise.allSettled([
      getSeniorsByUser(user?.id, 0),       // caregiver → gets seniors
      getCaregiverSeniorsList(),            // senior → gets caregivers
    ]);

    const caregiverData = results[0].status === 'fulfilled'
      ? (results[0].value?.data ?? []) : [];
    const monitorData = results[1].status === 'fulfilled'
      ? (results[1].value?.data ?? []) : [];
    // deduplicate by a unique user identifier across both arrays
    const seen = new Set();
    const merged = [...caregiverData, ...monitorData].filter(item => {
    // use whichever user ID field represents the OTHER person
    const uniqueId = item.senior_id || item.caregiver_id;
    if (seen.has(uniqueId)) return false;
    seen.add(uniqueId);
    return true;
    });
    return { data: merged };
    },
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
  if (status === 'error') return <div>Failed to load connections.</div>

  const seniors =data?.data ?? []

  return (
    <div>
      <h3>Your Connections</h3>

      {/* existing seniors list */}
      {seniors.length === 0 ? (
        <p>No connections yet. Add one below!</p>
      ) : (
        seniors.map((senior) => (
          <SeniorCard key={senior.relationship_id || senior.caregiver_id}  
          senior={senior} />
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
        <Button onClick={() => setShowForm(true)}>
          + Add Connection
        </Button>
      )}
    </div>
  );
}