## Getting Started

Make sure you have docker desktop installed. First clone the repo and then run below command

```bash
 docker-compose up -d --build
```

Open [http://localhost:8501](http://localhost:8501) with your browser to see the dashboard.


## What each code does 

publisher: publish data to MQTT in UNS format
subscriber: publish data to MongoDB from MQTT
dashbord: display the KPI from UNS

## How to stop 
```bash
 docker-compose down
```