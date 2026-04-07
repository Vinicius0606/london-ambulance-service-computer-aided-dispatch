from IATriagem import IATriagem
from triagem import Triagem

teste = IATriagem()

mensagem = r"""
    
    Socorro, meu cachorro está passando mal, e minha mãe está vomitando muito e com dor de cabeça, esta sem conseguir respirar
"""
ocorrencia = teste.extrairOcorrencia(mensagem)

print("\n")
print(ocorrencia)
print("\n")

resultado_triagem = teste.analisarOcorrencia(ocorrencia)

prioridade = teste.definirPrioridade(resultado_triagem)

ambulancias = teste.calcularQuantidadeAmbulancias(ocorrencia["quantidade_vitimas"], prioridade)

print(f"Resultado Triagem: {resultado_triagem}\nPrioridade: {prioridade}\nAmbulancias: {ambulancias}")

triagem = Triagem(ocorrencia, prioridade, ambulancias["qtdAmbulancias"], ambulancias["ambulancia"])