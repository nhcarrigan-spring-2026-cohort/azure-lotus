import useTitle from '../components/hooks/useTitle';
import './about.css'
import warning from '../assets/warning.png'
import green from '../assets/green-button.png'
import red from '../assets/red-button.png'
import boy from '../assets/boy-circle.png'
import girl from '../assets/girl-circle.png'
import grandpa from '../assets/grandpa-full.png'

export default function about() {
  useTitle('About');
  return (
    <div className='about-page'>
      <div className='container-about'>
        <div className='textbox-about' id='one-about'>1. Seniors open the app and click one of two buttons</div>

        <div className='mobile-row' id='buttons-row'>
          <img src={green} className='btns-about' id='green-btn-about'/>
          <img src={red} className='btns-about' id='red-btn-about'/>
        </div>

        <div className='textbox-about' id='two-about'>2. If a specific time exceeds, it automatically indicates that Senior needs help</div>

        <div className='mobile-row' id='people-row'>
          <img src={girl} className='circles' id='girl-about'/>
          <img src={boy} className='circles' id='boy-about'/>
        </div>

        <div className='textbox-about' id='three-about'>3. Caregiver / volunteer would get notified</div>
        <div className='textbox-about' id='four-about'>4. Volunteers could check upon more that one senior</div>

        <img src={grandpa} id='grandpa-about'/>
        <div className='textbox-about' id='five-about'>5. and of course, Senior can use the app to alert you when they need</div>

        <img src={warning} id='warning-about'/>
      </div>
    </div>
  );
}
