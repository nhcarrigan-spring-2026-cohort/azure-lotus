import './Card.css';


export default function Card({children, className, onClick, title, ...props}) {

    const cardClass = `card ${className}`;

    return (
        <div className={`card-container`}>
            <div className={`${cardClass}`} onClick={onClick} {...props}>
                <h2>{title}</h2>
                {children}
            </div>
        </div>
    )
}