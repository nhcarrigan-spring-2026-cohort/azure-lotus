import Card from '../components/ui/Card';
import './DashboardCards.css'
import React, { useEffect, useState } from 'react';
import { getSeniorsByUser } from '../api/senior.js';
import { useAuthContext } from '../context/AuthContext';

export default function DashboardCards({date}) {
    const { user, accessToken } = useAuthContext();
    const caregiverId = user.id;

    const [seniorsData, setSeniorsData] = useState([]);
    const [loading, setLoading] = useState(true);
    const whichDay = date;
    
    useEffect(() => {
        if (!user?.id || !accessToken) return;
        const getData = async () => {
            setLoading(true);
            try {
                const result = await getSeniorsByUser(caregiverId, whichDay);
                if (result.success) {
                    setSeniorsData(result.data)
                    console.log("Fresh data from API:", result.data);
                }
            } catch (error) {
                throw error.response?.data || error.message || error;
            } finally {
                setLoading(false);
            }
        };
        getData();
    },[whichDay, caregiverId, accessToken]);

    if (loading) return <p>Loading...</p>;

    if (!seniorsData || seniorsData.length === 0) {
        return (
            <div className="cards-board">
                <Card key="zero card" first_name="No" last_name="Seniors Found" />
            </div>
        );
    }


    return (
        <div className="cards-board">
            {seniorsData.map((senior, index) => (
                <Card 
                    key={senior.id || index} 
                    {...senior}
                />
            ))}
        </div>
    );
}