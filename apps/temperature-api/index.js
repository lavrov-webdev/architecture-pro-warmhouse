const express = require('express');

const app = express();
const port = process.env.PORT || 8081

const DATA_BASE = [
    {
        sensorId: 1,
        location: 'Living Room',
        value: 20,
        unit: '°C',
        status: 'active',
        createdAt: new Date(),
        updatedAt: new Date()
    },
    {
        sensorId: 2,
        location: 'Bedroom',
        value: 22,
        unit: '°C',
        status: 'active',
        createdAt: new Date(),
        updatedAt: new Date()
    },
    {
        sensorId: 3,
        location: 'Kitchen',
        value: 24,
        unit: '°C',
        status: 'active',
        createdAt: new Date(),
        updatedAt: new Date()
    }
]

setInterval(() => {
    for (const item of DATA_BASE) {
        item.value = Math.floor(Math.random() * 100);
    }
}, 1000);

app.get('/temperature', (req, res) => {
    const sensorId = req.query.sensorId;
    const location = req.query.location;
    if (!sensorId && !location) {
        return res.status(400).json({ error: 'Sensor ID or location are required' });
    }
    let value = null;
    if (sensorId) {
        const sesnor = DATA_BASE.find(item => item.sensorId === +sensorId);
        if (!sesnor) {
            return res.status(404).json({ error: 'Sensor with ID ' + sensorId + ' not found' });
        }
        value = sesnor.value;
        
    }
    if (location) {
        const sesnor = DATA_BASE.find(item => item.location === location);
        if (!sesnor) {
            return res.status(404).json({ error: 'Location "' + location + '" not found' });
        }
        value = sesnor.value;
    }
    res.json({ value });
});

app.listen(port, () => {
    console.log(`Temperature API listening on port ${port}`);
});