def normalizar_coordenadas(latitude, longitude) -> tuple[float, float] | None:
    if isinstance(latitude, bool) or isinstance(longitude, bool):
        return None
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError, OverflowError):
        return None

    if -90 <= latitude <= 90 and -180 <= longitude <= 180:
        return latitude, longitude
    return None


class Endereco:

    def __init__(self, CEP: str, logradouro:str, bairro:str, cidade:str, 
                estado:str, latitude:float, longitude:float, complemento:str | None = None, numero:int | None = None):
        
        self.id = None
        self.CEP = CEP
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.complemento = complemento
        self.latitude = latitude
        self.longitude = longitude
    
    def atualizar_ID(self, id: int):

        self.id = id