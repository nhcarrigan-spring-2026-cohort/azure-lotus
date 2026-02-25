import useTitle from '../components/hooks/useTitle';
import SeniorList from '../components/settings/SeniorList';

export default function signup() {
    useTitle('Senior Check | Settings');
    return (
        <>
            <SeniorList />
        </>
    );
}