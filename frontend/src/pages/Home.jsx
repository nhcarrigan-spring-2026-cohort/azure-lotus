import useTitle from '../components/hooks/useTitle';
/* import Card from '../components/ui/Card'; */
/* import CheckIn from '../components/checkin/CheckIn'; */
import HomeSenior from './HomeVariations/HomeSenior/HomeSenior.jsx';
import './Home.css';
import { useAuthContext } from '../context/AuthContext.jsx';
import HomeGuest from './HomeVariations/HomeVisitor/HomeGuest.jsx';

export default function Home() {
  const { user, isAuthenticated } = useAuthContext();
  useTitle();

  return (
    <>
      {/* <h1>Home</h1> */}
        {isAuthenticated ? (
        <>
          <HomeSenior />
        </>
      ) : (
            <HomeGuest/>
        )}
    </>
  );
}
