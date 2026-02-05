import React, { useEffect } from "react";


const useTitle = (title) => {
    useEffect(() => {
        document.title = (title) ? `Senior Checkin - ${title}` : "Senior Checkin";
    }, []);
};

export default useTitle;