import Card from '../components/ui/Card';
import './DashboardCards.css'

const mockData = {
    0: [
        {name: "Jaafar", status: "waiting", time: "9:00"},
        {name: "aeki", status: "waiting", time: "8:00"},
        {name: "Notcori", status: "missed", time: "7:30"},
        {name: "Leo", status: "checked in", time: "7:00"}
    ]
    ,
    1 : [
        {name: "Jaafar", status: "checked in", time: "9:00"},
        {name: "aeki", status: "missed", time: "8:00"},
        {name: "Notcori", status: "checked in", time: "7:30"},
        {name: "Leo", status: "missed", time: "7:00"}
    ],
    
    2 : [
        {name: "Jaafar", status: "missed", time: "9:00"},
        {name: "aeki", status: "missed", time: "8:00"},
        {name: "Notcori", status: "missed", time: "7:30"},
        {name: "Leo", status: "missed", time: "7:00"}
    ]
}

export default function DashboardCards({date}) {



    if((!date  && date!==0)|| date >= Object.keys(mockData).length ) return(
        <div className="cards-board">
                <Card key="zero card"/>
        </div>
    );


    return(
        <div className="cards-board">
            {mockData[date].map( card => (
                <Card key={`${card.name}-${card.time}-${card.date}`} {...card}/>
            ))}
        </div>
    );
}