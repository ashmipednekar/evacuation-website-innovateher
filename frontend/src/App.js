import React, { useState, useEffect } from 'react';

function App() {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch('/')
            .then(response => response.json())
            .then(data => setData(data));
    }, []);

    return (
        <div>
            {data ? <p>{data.message}</p> : <p>Loading...</p>}
        </div>
    );
}

export default App;