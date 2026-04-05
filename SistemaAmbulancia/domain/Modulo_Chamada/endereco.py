class Endereco:

    def __init__(self, id: int, CEP: str, logradouro:str, bairro:str, cidade:str, 
                estado:str, latitude:float, longitude:float, complemento:str | None = None, numero:int | None = None):
        
        self.id = id
        self.CEP = CEP
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.complemento = complemento
        self.latitude = latitude
        self.longitude = longitude