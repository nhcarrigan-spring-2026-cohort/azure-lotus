import useTitle from '../components/hooks/useTitle';
import Card from '../components/ui/Card';
import './Home.css';

export default function Home() {
  useTitle();
  return (
    <>
      <h1>Home</h1>
    </>
  );
}
