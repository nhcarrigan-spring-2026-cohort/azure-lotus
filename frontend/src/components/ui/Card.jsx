import './Card.css';



// Instructions

/*
    Create a reusable card component in components/UI
-Simple styled container DONE
-Card should accept an optional onClick prop to make it clickable when needed. DONE
-Card should accept an optional classname to make additional (custom)styling
-Card should be responsive 
-Card should accept children so that we can put any content inside it. DONE

*/


export default function Card({children, className, onClick, ...props}) {

    const cardClass = `card ${className}`;

    return (
        <div className={`card-container`}>
            <div className={`${cardClass}`} onClick={onclick} {...props}>
                <h1>Card component</h1>
                {children}
            </div>
        </div>
    )
}