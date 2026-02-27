import React, { useState, useRef, useEffect } from 'react';
import './HistorySlider.css';
 /* 
    IMPORTANT!!

    how this copmponent works
    1- This copmponent shows 7 days that are [Day-7,...Day-2, Yesterday, Today] this order
    the [dates] also includes two empty buffers form each arrany ends. so dates = ["", Day-7,...Day-2, Yesterday, Today, ""]
        1-A: Day-N format is like : Tue, Feb 22
        1-B: Later we will use a technique so get the actual indexed to make <HistorySlider /> communicate with other components using the selected date. 

    2- Handling scroll and click:
        2-A you can scroll by clicking arrows
        2-B you can scroll by clicking left of right dimmed dates

        Handling scoll and click are crucial for passing {onDateSelect} value to other components like <DashboardCards />
    
    3- reverse [dates]index logic happens by applying: "arithmetic: (arrRange-offset)" 
                                                                    where (arrRange= HISTORY_RANGE-1)
                                                                    and (offset = clickedIndex - 1)
                                                                    where (clickedIndex=the actual index that is currently being chosen by user)
 
    4- final output (one of these values): 
                    Today = 0, Yesterday = 1, Day-2 = 2, Day-3 = 3
                        OR like:
                    Day-3 = 3 , Day-2 = 2, Yesterday = 1, Today = 0
 


    Long Story Short : <HistorySlider onDateSelect={setSelectedDate} /> returns     setSelectedDate as number value,  Today = 0, Yesterday = 1, Day-2 = 2, Day-3 = 3                               
*/

export default function HistorySlider( {onDateSelect}) {

    const HISTORY_RANGE = 7    // 7 days back in time

    
    // Generating date range of 7 + 2 buffer at each end.
    const arrRange = HISTORY_RANGE-1
    const [dates] = useState(() => {
        const result = [];
        const options = { weekday: 'short', month: 'short', day: 'numeric' };
        
        for (let i = arrRange; i >= 0; i--) {
            const d = new Date();
            d.setDate(d.getDate() - i);
            
            let label;
            if (i === 0) label = "Today";
            else if (i === 1) label = "Yesterday";
            else label = d.toLocaleDateString('en-US', options);
            
            result.push(label);
        }
        return ["", ...result, ""]; // Buffer left and right
    });

    const [activeIndex, setActiveIndex] = useState(dates.length - 2); // -2 because of the two empty buffers
    const scrollRef = useRef(null);     // essential for the whole slider visualization

    // initial positioning to "Today"
    useEffect(() => {
        const slider = scrollRef.current;
        if (slider) {
            const itemWidth = slider.offsetWidth / 3;
            // Scroll so "Today" (2nd to last)
            slider.scrollLeft = (dates.length - 3) * itemWidth;
        }
    }, [dates]);   /* Dependency [dates]: Ensures this runs only when dates is ready. Since dates is static, this effectively runs once.  */

    const handleScroll = () => {
        const slider = scrollRef.current;
        const itemWidth = slider.offsetWidth / 3;
        const centerIndex = Math.round(slider.scrollLeft / itemWidth) + 1;
        
        if (centerIndex !== activeIndex) {
            setActiveIndex(centerIndex);
            const offset = centerIndex - 1;
            if (onDateSelect && offset >= 0 && offset <= 6) {
            onDateSelect(arrRange-offset);
            }
        }

        
    };

    const slide = (direction) => {
        const slider = scrollRef.current;
        const itemWidth = slider.offsetWidth / 3;
        slider.scrollBy({ left: direction * itemWidth, behavior: 'smooth' });
    };

    const handleItemClick = (clickedIndex) => {
        if (clickedIndex < activeIndex) {
            slide(-1); // Move left
        } else if (clickedIndex > activeIndex) {
            slide(1);  // Move right
        }

        /* if (onDateSelect && dates[clickedIndex]) {
        onDateSelect(dates[clickedIndex]); // e.g., "Today", "Mon 6"
        } */

        const offset = clickedIndex - 1;
       if (onDateSelect && offset >= 0 && offset <= 6) {
        onDateSelect(arrRange-offset); // ✅ Send number: 0, 1, 2...
    }

};

    return (
        <div className="history-container">
            <button className="nav-arrow" onClick={() => slide(-1)}>‹</button>
            <div 
                className="slider-window" 
                ref={scrollRef} 
                onScroll={handleScroll}
            >
                {dates.map((date, index) => (
                    <div 
                        key={index} 
                        className={`slider-item ${activeIndex === index ? 'active' : 'dimmed'}`}
                        onClick={() => handleItemClick(index)}
                    >
                        {date}
                    </div>
                ))}
            </div>
            <button className="nav-arrow" onClick={() => slide(1)}>›</button>
        </div>
    );
}