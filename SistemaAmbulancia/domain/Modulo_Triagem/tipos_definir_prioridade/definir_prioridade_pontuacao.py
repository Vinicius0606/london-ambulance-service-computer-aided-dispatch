from .interface_definir_prioridade import Interface_definir_prioridade

class Definir_prioridade_pontuacao(Interface_definir_prioridade):

    def definir_prioridade(self, ocorrencia: dict):

        pontuacao = 0
        justificativa = []
        resultado = {}

        if not ocorrencia["respira"]:

            pontuacao = 90
            justificativa.append("parada respiratoria")

        elif ocorrencia["sangramento_intenso"]:

            pontuacao = 90
            justificativa.append("sangramento intenso")
      
        elif ocorrencia["quantidade_vitimas"] >= 2 and ocorrencia["suspeita_trauma"]:
            pontuacao = 90
            justificativa.append(f"{ocorrencia['quantidade_vitimas']} vitimas e suspeita de trauma")

        if ocorrencia["suspeita_trauma"]:
            pontuacao += 60
            justificativa.append("suspeita de trauma")
        
        if ocorrencia["inconsciente"]:
            pontuacao += 50
            justificativa.append("vitima inconsciente")
        
        if ocorrencia["dificuldade_respiratoria"]:

            pontuacao += 40
            justificativa.append("Dificuldade respiratoria")

        if ocorrencia["quantidade_vitimas"] >= 2:
            pontuacao += 30
            justificativa.append(f"{ocorrencia['quantidade_vitimas']} vitimas")

        elif ocorrencia["quantidade_vitimas"] == 1:
            pontuacao += 20
            justificativa.append("1 vitima")

        else:
            pontuacao += 10
            justificativa.append("Transporte de incapacitado")
        
        resultado = {
            "pontuacao": pontuacao,
            "justificativa": justificativa
        }

        prioridade = self.definir_pontuacao_em_prioridade(resultado)

        return prioridade

    def definir_pontuacao_em_prioridade(self, resultado_triagem: dict):

        prioridade = 0
        
        if resultado_triagem["pontuacao"] <= 10:
            prioridade = 1

        elif resultado_triagem["pontuacao"] > 10   and resultado_triagem["pontuacao"] < 60:
            prioridade = 2

        elif resultado_triagem["pontuacao"] >= 60 and resultado_triagem["pontuacao"] < 90:
            prioridade = 3

        else:
            prioridade = 4

        return prioridade