import ollama

def enviar_mensagem_IA(prompt):

    resposta = ollama.chat(
            model="qwen3:8b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    
    return resposta