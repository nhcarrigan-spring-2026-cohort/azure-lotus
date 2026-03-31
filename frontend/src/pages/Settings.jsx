import { useNavigate } from 'react-router';
import useTitle from '../components/hooks/useTitle';
import SeniorList from '../components/settings/SeniorList';
import Button from '../components/ui/Button';

export default function Settings() {
  useTitle('Settings');
  const navigate = useNavigate();

  return (
    <>
      <h2>Settings</h2>
      <SeniorList />
    <div style={{ display: 'flex', gap: '35px', marginTop: '35px' }}>
    <Button
        onClick={() => navigate('/checkin')}        // ← added: go to HomeSenior (checkin)
      >
        Continue to Check-in
      </Button>

      </div>
    </>
    
  );
}