import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import pyttsx3
import openai  # Biblioteca para acessar a API OpenAI
import os
import random

# Configuração da API OpenAI com variável de ambiente
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    API_KEY = simpledialog.askstring("Chave da API", "Digite sua chave da API OpenAI:")
    if API_KEY:
        os.environ["OPENAI_API_KEY"] = API_KEY
    else:
        messagebox.showerror("Erro", "A chave da API OpenAI é necessária para continuar.\n\nAcesse https://platform.openai.com/account/api-keys para gerar sua chave.")
        exit()

openai.api_key = API_KEY

# Inicializa o motor de síntese de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Ajusta a velocidade da fala

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

contador_perguntas = 0  # Inicializa contador

# Lista de examinadores com base no currículo Lattes
banca = {
    "Josefina Barrera Kalhil": [
        "Como sua pesquisa pode contribuir para a melhoria da formação continuada dos professores ribeirinhos?",
        "Quais desafios os professores enfrentam ao aplicar essa tecnologia na prática pedagógica?"
    ],
    "Whasgthon Aguiar Almeida": [
        "Como os podcasts podem ser adaptados à realidade das escolas ribeirinhas, considerando as dificuldades tecnológicas da região?",
        "O que diferencia o uso de podcasts de outras estratégias tecnológicas na educação?"
    ],
    "Lucinete Gadelha Costa": [
        "Como você pretende avaliar a eficácia dessa metodologia?",
        "Qual é a importância da oralidade e da contação de histórias na educação amazônica?"
    ]
}

# Função para gerar perguntas sequenciais e exibir o examinador
def gerar_pergunta():
    global contador_perguntas
    contador_perguntas += 1
    examinador = random.choice(list(banca.keys()))
    pergunta = random.choice(banca[examinador])
    texto_pergunta = f"Pergunta {contador_perguntas}: {examinador}\n{pergunta}"
    pergunta_label.config(text=texto_pergunta)
    falar(texto_pergunta)
    return examinador

# Função para avaliar a resposta e gerar uma nota
def avaliar_resposta():
    resposta = resposta_entry.get("1.0", tk.END).strip()
    if not resposta:
        messagebox.showwarning("Aviso", "Por favor, insira uma resposta antes de avaliar.")
        return
    
    criterios = {
        "Clareza": random.randint(6, 10),
        "Coesão": random.randint(6, 10),
        "Argumentação": random.randint(6, 10)
    }
    nota_final = sum(criterios.values()) // len(criterios)
    criterios_formatados = "\n".join([f"{k}: {v}/10" for k, v in criterios.items()])
    
    resposta_revisada = f"Critérios de avaliação:\n{criterios_formatados}\n\nNota final: {nota_final}/10"
    resposta_revisada_label.config(text=resposta_revisada)

    # Melhorar resposta utilizando OpenAI
    try:
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um avaliador acadêmico. Melhore a resposta fornecida otimizando clareza, coesão e argumentação."},
                {"role": "user", "content": resposta}
            ],
            temperature=0.7
        )
        resposta_melhorada = response["choices"][0]["text"].strip()
    except Exception as e:
        resposta_melhorada = f"Erro ao processar melhoria da resposta: {str(e)}\n\nSugestão: Atualize a API OpenAI com 'pip install openai --upgrade' ou instale a versão correta com 'pip install openai==0.28'."
    resposta_melhorada_text.config(state=tk.NORMAL)
    resposta_melhorada_text.delete("1.0", tk.END)
    resposta_melhorada_text.insert(tk.END, resposta_melhorada)
    resposta_melhorada_text.config(state=tk.DISABLED)

# Criando a interface gráfica
root = tk.Tk()
root.title("Ethel - Simulação da Banca Examinadora")
root.geometry("600x800")
root.iconbitmap("icone.ico")

# Adicionando os elementos gráficos
tk.Label(root, text="Simulação da Banca Examinadora", font=("Times New Roman", 14, "bold")).pack(pady=10)
pergunta_label = tk.Label(root, text="Clique em 'Gerar Pergunta' para iniciar", font=("Times New Roman", 12), wraplength=550, justify="left")
pergunta_label.pack(pady=10)

btn_gerar = tk.Button(root, text="Gerar Pergunta", command=gerar_pergunta, font=("Times New Roman", 12))
btn_gerar.pack(pady=5)

resposta_entry = scrolledtext.ScrolledText(root, height=5, width=70, font=("Times New Roman", 12))
resposta_entry.pack(pady=10)

btn_avaliar = tk.Button(root, text="Avaliar Resposta", command=avaliar_resposta, font=("Times New Roman", 12))
btn_avaliar.pack(pady=5)

resposta_revisada_label = tk.Label(root, text="Resposta revisada aparecerá aqui", font=("Times New Roman", 12), wraplength=550, justify="left")
resposta_revisada_label.pack(pady=10)

resposta_melhorada_text = scrolledtext.ScrolledText(root, height=5, width=70, font=("Times New Roman", 12))
resposta_melhorada_text.pack(pady=10)
resposta_melhorada_text.config(state=tk.DISABLED)

btn_copiar_melhorada = tk.Button(root, text="Copiar Resposta Melhorada", command=lambda: root.clipboard_append(resposta_melhorada_text.get("1.0", tk.END)), font=("Times New Roman", 12))
btn_copiar_melhorada.pack(pady=5)

root.mainloop()
