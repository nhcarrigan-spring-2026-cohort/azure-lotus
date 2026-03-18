import useTitle from '../components/hooks/useTitle';
import HomeSenior from './HomeVariations/HomeSenior/HomeSenior.jsx'
import HomeGuest from './HomeVariations/HomeVisitor/HomeGuest.jsx'
import './Home.css';
import { useAuthContext } from '../context/AuthContext.jsx';

export default function Home() {
  useTitle();
  const {isAuthenticated } = useAuthContext();
  
  console.log('Home renders, isAuthenticated:', isAuthenticated)  // ← add
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