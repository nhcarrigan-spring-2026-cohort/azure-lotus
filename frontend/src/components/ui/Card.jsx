import { Children } from 'react';
import './Card.css';

/*
    Card Component will need adjusments later based on the job it does

*/
export default function Card({ 
    senior_first_name, 
    senior_last_name, 
    status, 
    senior_time, 
    senior_phone,
    ...children 
}) {

    const fullName = senior_first_name && senior_last_name
        ? `${senior_first_name} ${senior_last_name}` 
        : (senior_first_name || senior_last_name || 'No Senior Name');
        
    //const cardClass = `card ${className}`; //  @j3farsale7: this was build in the past, I don't know why to use {children, className, onClick} for now 
    function statusIcon() {
        if (status === "missed") return '❌';
        if (status === "completed" || status === "checked in") return '✔️';
        if (status === "waiting") return '⌛';
        return '❓';
    }

    return (

             <div className="dashboard-card-main-container"> 
                    <div className='senior-name'>{ fullName || 'no Senior name'}</div> 
                    <div className='icon-status-time'> 
                        <div className='icon' title={status}>{statusIcon()}</div>
                        <div className='status'>{status || 'noData'}</div>
                        <div className='time'>{senior_time || 'noData'}</div>
                    </div>
                    <div className='call-button' title={`Call ${senior_phone || 'N/A'}`}>📞</div>
                    <div className='message-button' title={`Message ${senior_phone || 'N/A'}`}>💬</div>

            </div>

    )
}