import { useNavigate } from 'react-router';
import useTitle from '../components/hooks/useTitle';
import SeniorList from '../components/settings/SeniorList';
import Button from '../components/ui/Button';

export default function signup() {
  useTitle('Settings');
  const navigate = useNavigate();

  return (
    <>
      <h2>Settings</h2>
      <SeniorList />
      <Button
        // TODO:  confirm page name and add a new page
        onClick={() => navigate('/add-connection')}
      >
        Add Connection
      </Button>
    </>
  );
}
