# Platformă IoT folosind Microservicii
Acest proiect implementeaza un sistem IoT pentru colectarea si stocarea datelor 
senzorilor utilizand microservicii orchestrate prin Docker Swarm

## Microserviciile utilizate / create
- Adapter (Paho MQTT + InfluxDB Client): Un serviciu Python care asculta mesaje 
MQTT primite de la senzori si le stocheaza in baza de date
- Baza de date (InfluxDB): unde se retin datele
- Broker MQTT (Eclipse Mosquitto): primeste date de la senzori si le publica pe 
diverse topicuri
- Platforma de vizualizare (Grafana): dashboard-uri personalizabile pentru 
analiza datelor

## Rularea codului
```
git clone https://github.com/irinacos/IoT-Sensor-Data-Platform.git
cd IoT-Sensor-Data-Platform
./run.sh
```
Comanda va construi imaginea adaptorului si va initializa Swarm, dupa care va 
implementa stack-ul de servicii descris mai sus.

## Adaptorul:
- se aboneaza la toate mesajele trimise (prin folosirea unui wildcard)
- procesarea mesajelor este gestionata cu ajutorul functiei on_message
- folosind un logger, sunt astfel afisate mesajele de logging (in urma 
introducerii unor date). Mesajele pot fi observate ruland "docker service logs 
nume_serviciu". Totusi, aceste mesaje sunt vizibile doar daca variabila de mediu 
DEBUG_DATA_FLOW este setata pe true (default)
- sunt introduse in baza de date cheile care au valori numerice
- daca nu este specificat un timestamp in payload, se foloseste timpul curent
(am folosit UTC)
- stocheaza datele primite in baza de date, conexiunile fiind realizate cu ajutor 
variabilelor de mediu

## Persistenta datelor
Folosirea volumelor Docker pentru ca datele si configuratiile din InfluxDB, MQTT 
Broker si Grafana sa nu se piarda chiar daca containerele este oprit/repornit.

## Trafic intre containere
Folosirea unor retele izolate (driver overlay) de containere:
- mqtt_network: adapter, mqtt_broker
- db_network: adapter, influxdb, grafana
