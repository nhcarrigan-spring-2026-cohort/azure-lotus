export default function SeniorCard({senior}) {
    console.log(senior)
    return (
        <div className="senior-card">
            <h2>{`${senior.firstname} ${senior.lastname}`}</h2>

        </div>
    );
}