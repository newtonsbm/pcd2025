from typing import Union
import random

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/piadas")
def get_piada():
    piadas_list = [
        "Por que os programadores confundem Halloween com Ano Novo? Porque 31 de outubro é 1º de janeiro.",
        "Qual a melhor linguagem de programação para aqueles que gostam de fazer programas que nem funcionam? Assembly."
        "Por que os desenvolvedores preferem dark mode? Porque a luz atrai bugs!",
        "Um programador sai para jantar com a esposa. Ela pergunta: 'Você quer ir ao restaurante A ou B?' Ele responde: 'Sim.'",
        "Como você chama um programador que não toma banho? Um desenvolvedor de código sujo.",
        "Por que os programadores odeiam a natureza? Ela tem muitos bugs e não tem WiFi.",
        "Qual é a diferença entre um programador e um usuário comum? O programador acha que o problema está no código, o usuário acha que o problema está no computador.",
        "Por que os programadores usam óculos escuros? Para não serem reconhecidos em produção.",
        "Quantos programadores são necessários para trocar uma lâmpada? Nenhum, isso é um problema de hardware.",
        "O que um programador faz quando está com fome? Ele pede uma pizza recursivamente até esgotar a memória.",
        "Por que os arrays começam do zero? Porque os programadores contam os anos de experiência da mesma forma.",
        "Qual é o animal favorito de um programador? O Python, porque não morde e é fácil de lidar."
    ]
    return random.choice(piadas_list)
