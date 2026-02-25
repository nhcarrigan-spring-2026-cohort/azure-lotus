import useTitle from '../components/hooks/useTitle';
import CreateAccount from '../components/CreateAccount';

export default function signup() {
  useTitle('Sign Up');
  return (
    <>
      <CreateAccount/>
    </>
  );
}
