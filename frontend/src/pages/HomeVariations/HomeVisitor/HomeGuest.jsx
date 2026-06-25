import { useNavigate } from 'react-router';
import './HomeGuest.css';
import HomeImageCharacters from './HomeImageCharacters';
import ThemeButton from '../../../components/ui/ThemeButton.jsx';


export default function HomeGuest(){
    const navigate = useNavigate();
    return (
        <div className='container-HomeGuest'>
            <div className='leftdown'>
                <p id='maintalk'>Connecting and Caring for Seniors</p>
                <div id='theme-btn-imported'><ThemeButton text='Sign Up' onClick={() => navigate('/signup')}/></div>
            </div>
            <div className='rightup'>
                <HomeImageCharacters />
            </div>
        </div>
    )
}