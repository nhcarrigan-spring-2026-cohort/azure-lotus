import './HomeImageCharacters.css';

export default function HomeImageCharacters() {
    return (
        <div className='container-HomeImageCharacters'>
            <img src='src/assets/girl-circle.png'
                 className='characters-circle'
                 id='girl'
            />
            <img src='src/assets/boy-circle.png'
                 className='characters-circle'
                 id='boy'
            />
            <img src='src/assets/man-circle.png' 
             className='characters-circle'
             id='man'
             />

            <img src='src/assets/granny-full.png'
                 id='granny'
            />

            <img src='src/assets/green-button.png' 
                 className='show-btn'
                 id='green'
            />
            <img src='src/assets/red-button.png' 
                 className='show-btn'
                 id='red'
            />
        </div>
    )
}