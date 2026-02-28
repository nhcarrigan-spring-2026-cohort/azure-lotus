import useTitle from '../components/hooks/useTitle';
import './Dashboard.css';
import HistorySlider from '../components/ui/HistorySlider';
import DashboardCards from '../components/DashboardCards';
import {useState} from 'react';

/* 
    dashboard is a flex-column-down that has TWO major compnents:
    1- on top a HistorySlider that points to TODAY by defualt, user can choose today or yesterday or previos days up to 7 :
    1-  <  Yesterday Today        >
        <  Sun, Feb 22  Yesterday Today >
        <  Sat, Feb 21  Sun, Feb 22  Yesterday >


    2- DashboardCards which is a inner flex-column-down that covers most of the page in the center, contains status cards
    2- Senior status card:

    
        --------------------------------------
        |  Senior name        |  ICON        |
        |                     |  status      |
        | call-btn  msg-btn   |  time        |
        --------------------------------------   
    

    <HistorySlider /> communicate with <DashboardCards />  through selectedDate state
             
 */

export default function Dashboard() {
  useTitle('Dashboard');
  const [selectedDate, setSelectedDate] = useState(0);

  return (
    <div className='dashboard-content'>  {/*main felx-down*/}
      <HistorySlider onDateSelect={setSelectedDate} />
      <DashboardCards date={selectedDate} />
    </div>
  );
}
