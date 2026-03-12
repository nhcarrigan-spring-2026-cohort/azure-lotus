import './HomeGuest.css';
import HomeImageCharacters from './HomeImageCharacters';
import ThemeButton from '../../../components/ui/ThemeButton.jsx';


export default function HomeGuest(){
    return (
        <div className='container-HomeGuest'>
            <div className='leftdown'>
                <p id='maintalk'>Connecting and Caring for Seniors</p>
                <div id='theme-btn-imported'><ThemeButton text='Sign Up'/></div>
            </div>
            <div className='rightup'>
                <HomeImageCharacters />
            </div>
        </div>
    )
}