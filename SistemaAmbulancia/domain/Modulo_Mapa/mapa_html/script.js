const latitudeCentro = -15.834400;
const longitudeCentro = -47.911496;

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

    adicionar_rota(latitude, longitude){

        this.marker.on("click", (evento) => {
            L.DomEvent.stopPropagation(evento)

            desenhar_rota_real(
                [latitude, longitude],
                [this.latitude, this.longitude]
            );
        });
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

                this.marker.setIcon(ambulanciaDisponivelIcon);
            
            }else if(status === "Atendendo"){

                this.status = status;

                this.marker.setIcon(ambulanciaAtendendoIcon);
            
            }else if(status === "Indisponivel"){

                this.status = status;

                this.marker.setIcon(ambulanciaIndisponivelIcon);
            }

        }
    }
}

class Chamada{

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
            { icon: chamadaPendenteIcon}

        ).addTo(map)
    }

    atualizar_status(status){

        if(this.marker){

            this.status = status;

            this.marker.setIcon(chamadaPendenteIcon);
        }
    }
}


async function desenhar_rota_real(origem, destino){

    const url = `https://router.project-osrm.org/route/v1/driving/${origem[1]},${origem[0]};${destino[1]},${destino[0]}?overview=full&geometries=geojson`;
    
    const resposta = await fetch(url);

    const dados = await resposta.json();

    remover_rota_atual();

    const rota = L.geoJSON(dados.routes[0].geometry, {
        style: {
            color: "blue",
            weight: 5
        }
    }).addTo(map);

    rotaAtual = rota;

    map.fitBounds(rota.getBounds());
}

function adicionar_ambulancia(id, latitude, longitude, status){

    const ambulancia = new Ambulancia(id, latitude, longitude, status);

    ambulancia.adicionar_marker(map);

    ambulancias.push(ambulancia);
}

function adicionar_rota_ambulancia(id, latitudeD, longitudeD){

    const ambulancia = ambulancias.find(a => a.id === id)

    if(!ambulancia) return null;

    ambulancia.adicionar_rota(latitudeD, longitudeD)
}

function adicionar_chamada(id, latitude, longitude, status){

    const chamada = new Chamada(id, latitude, longitude, status);

    chamada.adicionar_marker(map)

    chamadas.push(chamada)

}

function mover_ambulancia(id, latitude, longitude) {
    
    const ambulancia = ambulancias.find(ambulancia => ambulancia.id === id);

    if (ambulancia) {
    
        ambulancia.mover(latitude, longitude);
    }
}

function remover_rota_atual(){
    
    if(rotaAtual){

        map.removeLayer(rotaAtual);

        rotaAtual = null;
    }
}

function atualizar_status(id, status){

    const ambulancia = ambulancias.find(a => a.id === id)

    if(!ambulancia) return null;

    ambulancia.atualizar_status(status)

}


const ambulancias = [];

const chamadas = [];

let rotaAtual = null;

const map = L.map('map', {
    zoomControl: true
}).setView([latitudeCentro, longitudeCentro], 18);

map.on("click", function(){
    remover_rota_atual();
});

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

areaOperacao.on("click", function(){
    remover_rota_atual()
});

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

const chamadaPendenteIcon = L.icon({
    iconUrl: "./assets/chamada.png",
    iconSize: [24, 24],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16]
})
