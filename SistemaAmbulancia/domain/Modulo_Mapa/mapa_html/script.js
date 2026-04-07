const latitudeCentro = 51.519378;
const longitudeCentro = -0.168820;

class Ambulancia{

    constructor(id, latitude, longitude, status){

        this.id = id;
        this.latitude = latitude;
        this.longitude = longitude;
        this.status = status;

        this.marker = null;
    }

    adicionar_marker(map) {
        
        this.marker = L.marker(

            [this.latitude, this.longitude],
            { icon: ambulanciaDisponivelIcon}

        ).addTo(map)
    }

    mover(latitude, longitude){

        this.latitude = latitude;
        this.longitude = longitude;

        if(this.marker){
            
            this.marker.setLatLng([latitude, longitude]);
        }
    }

    atualizar_status(status){

        if(this.marker){

            if(status === "Disponivel"){

                this.status = status;

                this.marker.setIcon("./assets/ambulance_disponivel.png");
            
            }else if(status === "Atendendo"){

                this.status = status;

                this.marker.setIcon("./assets/ambulance_atendendo.png");
            
            }else if(status === "Indisponivel"){

                this.status = status;

                this.marker.setIcon("./assets/ambulance_indisponivel.png");
            }

        }
    }
}

const ambulancias = [];

const map = L.map('map', {
    zoomControl: true
}).setView([latitudeCentro, longitudeCentro], 18);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
}).addTo(map);

const areaOperacao = L.circle([latitudeCentro, longitudeCentro], {
    radius: 10000,
    color: '#2563eb',
    fillColor: '#60a5fa',
    fillOpacity: 0.15,
    weight: 2
}).addTo(map);

areaOperacao.bindPopup('Área de operação: raio de 10 km');

const ambulanciaDisponivelIcon = L.icon({
    iconUrl: "./assets/ambulance_disponivel.png",
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16]
});

const ambulanciaAtendendoIcon = L.icon({
    iconUrl: "./assets/ambulance_atendendo.png",
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16]
});

const ambulanciaIndisponivelIcon = L.icon({
    iconUrl: "./assets/ambulance_indisponivel.png",
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16]
});

function adicionar_ambulancia(id, latitude, longitude, status){

    const ambulancia = new Ambulancia(id, latitude, longitude, status);

    ambulancia.adicionar_marker(map);

    ambulancias.push(ambulancia);
}

function mover_ambulancia(id, latitude, longitude) {
    
    const ambulancia = ambulancias.find(ambulancia => ambulancia.id === id);

    if (ambulancia) {
    
        ambulancia.mover(latitude, longitude);
    }
}