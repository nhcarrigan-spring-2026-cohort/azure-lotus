import SeniorCard from './SeniorCard';

export default function SeniorList() {

    const seniors = [
        { firstname: 'Patrick', lastname: 'Smith' },
        { firstname: 'John', lastname: 'Doe' },
        { firstname: 'Jane', lastname: 'Doe' },
    ]
    return (
        <div>
            {seniors.map(senior=> (
                <SeniorCard
                senior={senior}
            />))
            }
        </div>
    );
}