import './Card.css';

/*
    Card Component will need adjusments later based on the job it does

*/
export default function Card({children, className, onClick, name, status, time, ...props}) {

    const cardClass = `card ${className}`; //  @j3farsale7: this was build in the past, I don't know why to use {children, className, onClick} for now 
    function statusIcon(){
        if (status == "missed") {
            return '❌'
        }
        if (status == "checked in") {
            return '✔️'
        }
        if (status == "waiting") {
            return '⌛'
        }
        if (!status) return 'noData'
    }

    return (

             <div className="dashboard-card-main-container"> 
                    <div className='senior-name'>{ name || 'no Senior name'}</div> 
                    <div className='icon-status-time'> 
                        <div className='icon'>{statusIcon()}</div>
                        <div className='status'>{status || 'noData'}</div>
                        <div className='time'>{time || 'noData'}</div>
                    </div>
                    <div className='call-button'>📞</div>
                    <div className='message-button'>💬</div>

            </div>

    )
}