import useTitle from '../components/hooks/useTitle';
import CreateAccount from '../components/CreateAccount';
import HomeImageCharacters from './HomeVariations/HomeVisitor/HomeImageCharacters';
import './Signup.css';

export default function signup() {
  useTitle('Sign Up');
  return (
    <div className='container-Signupguest'>
      <div className='leftup'>
        <CreateAccount />
      </div>
      <div className='rightdown'>
        <HomeImageCharacters />
      </div>
    </div>
  );
}
