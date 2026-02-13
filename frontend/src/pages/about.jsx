import useTitle from '../components/hooks/useTitle';
import Card from '../components/ui/Card';

export default function about() {
  useTitle('About');
  return (
    <>
      <h1>About</h1>
    </>
  );
}
