import useTitle from '../components/hooks/useTitle';
/* import Card from '../components/ui/Card'; */
/* import CheckIn from '../components/checkin/CheckIn'; */
import HomeSenior from './HomeVariations/HomeSenior/HomeSenior.jsx';
import './Home.css';
import { useAuthContext } from '../context/AuthContext.jsx';
import HomeGuest from './HomeVariations/HomeVisitor/HomeGuest.jsx';

export default function Home() {
  useTitle();
  const { user, isAuthenticated } = useAuthContext();
  

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
