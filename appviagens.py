import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Inicializa para evitar NameError
resposta = None

# 🔑 Configure sua chave API
genai.configure(api_key="AIzaSyBG8Ui2Iq_a4m8_1WtTLykyiDXizSUuffs")

# 🔧 Use um dos modelos EXISTENTES
MODEL_NAME = "models/gemini-2.5-pro"
model = genai.GenerativeModel(MODEL_NAME)

# ---------------------------------------------------------
# 📌 Interface Streamlit
# ---------------------------------------------------------

st.title("✈️ Planejador Inteligente de Viagens")
st.write("Crie o roteiro da sua viagem com tudo o que você mais gosta!")


nome = st.text_input("Qual seu nome?")
destino = st.text_input("✨ Para onde você quer viajar?")
dias = st.number_input("📅 Quantos dias de viagem?", min_value=1, max_value=60)

estilo = st.selectbox(
    "🌎 Qual é o estilo da sua viagem?",
    ["Relax total 💆‍♀️", "Explorar tudo 🌍", "Gastronomia 🍽️", "Natureza 🌿", "Vida noturna 🎉", "Luxo ✨", "Baixo custo 💸", "Romântica ❤️"]
)

companhia = st.selectbox(
    "👥 Você vai viajar com quem?",
    ["Sozinho(a)", "Casal ❤️", "Família 👨‍👩‍👧", "Amigos 🧑‍🤝‍🧑"]
)

orcamento = st.selectbox(
    "💵 Qual é o orçamento aproximado por dia?",
    ["R$100–200", "R$200–400", "R$400–700", "R$700–1000", "R$1000+"]
)

atividade_top = st.text_input(
    "⭐ Sua atividade número 1 que você NÃO abre mão:"
)

restricoes = st.text_area(
    "⚠️ Alguma restrição, medo ou preferência importante?",
    placeholder="Ex: não gosto de trilha pesada, sou vegetariano, prefiro lugares tranquilos..."
)

ritmo = st.selectbox(
    "⏱️ Qual o ritmo ideal da viagem?",
    ["Leve (até 2 atividades por dia)", "Moderado (3–4 atividades por dia)", "Intenso (quero aproveitar cada minuto!)"]
)

transporte = st.selectbox(
    "🚗 Como pretende se locomover no destino?",
    ["A pé", "Uber/Taxi", "Carro alugado", "Transporte público"]
)


if st.button("Gerar Roteiro"):
    if not destino:
        st.warning("Digite um destino antes!")
    else:
        with st.spinner("Gerando roteiro..."):
            try:

                # 🔥 Aqui está o prompt DEFINITIVO
                prompt = f"""
Você agora é um EXPERT EM ROTEIROS DE VIAGENS PROFISSIONAL da região escolhida, super comunicativo, 
cheio de energia e expert em criar viagens inesquecíveis, vantajosas e com custo beneficio de dinheiro e tempo.

Crie um ROTEIRO COMPLETO para {dias} dias em **{destino}**, seguindo exatamente as regras abaixo:

===========================
🌟 1. ESTILO DA RESPOSTA  
===========================
- Não precisa se apresentar;
- Breve descrição do roteiro baseado nos gostos da pessoa;
- Direcione a fala para **{nome}**
- Linguagem direta, animada, acolhedora, empolgante e profissional.  
- Que soe como um guia local apaixonado pelo destino.  
- Texto fluido, claro e cheio de dicas valiosas.  
- Nada de texto genérico — tudo deve parecer específico e pensado para essa pessoa.

===========================
👤 2. PERSONALIZAÇÃO  
===========================
Leve em conta TUDO a seguir:

- Estilo da viagem: **{estilo}**
- Tipo de companhia: **{companhia}**
- Orçamento diário: **{orcamento}**
- Ritmo da viagem: **{ritmo}**
- Atividade indispensável: **{atividade_top}**
- Restrições e preferências: **{restricoes}**
- Transporte disponível no destino: **{transporte}**

===========================
📚 3. ESTRUTURA OBRIGATÓRIA  
===========================

### ✨ Visão Geral Épica da Viagem  
— um resumo cinematográfico do que a pessoa vai viver

### 🎒 Checklist Pré-Viagem  
- melhor época  
- o que levar  
- cuidados  
- apps úteis  
- transporte ideal  

### 📅 Roteiro Diário COMPLETO (para cada um dos {dias} dias)
Para cada dia, descreva:
- Manhã → atividade principal  
- Tarde → segunda atividade  
- Noite → jantar recomendado + atividade leve  
Inclua:
- horários
- versões alternativas (paga / gratuita)
- preços aproximados
- endereços
- duração média

### 🍽️ Gastronomia Imperdível  
— pratos típicos  
— restaurantes por faixa de preço  
— achadinhos locais  

### 📸 Pontos Instagramáveis  
— melhores horários  
— melhores ângulos  

### 🌙 Vida Noturna e Passeios Extras  
— rooftops, baladas, feirinhas, shows  

### 💰 Resumo Realista dos Custos  
— alimentação  
— transporte  
— passeios  
— extras  

### 💡 Dicas de Ouro do Guia Local  
— truques  
— como evitar filas  
— horários de ouro  
— golpes comuns da região  
— o que vale muito a pena x o que evitar  

===========================
🎯 4. FINALIZAÇÃO  
===========================
Termine com uma mensagem acolhedora, motivadora e com vibe de:
“Vai dar tudo certo, essa viagem vai ser INCRÍVEL.”
                """

                resposta_obj = model.generate_content(prompt)
                resposta = resposta_obj.text  # ← agora guarda texto corretamente

                st.success("Roteiro gerado com sucesso! ✨")
                st.write(resposta)

            except Exception as e:
            st.error(f"Erro ao gerar roteiro: {e}")

# ---------------------------------------------------------
# 📄 BOTÃO PARA BAIXAR O PDF
# ---------------------------------------------------------

if resposta:  # ← Agora sempre funciona sem erro
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for linha in resposta.split("\n"):
        pdf.multi_cell(0, 10, linha)

    pdf.output("roteiro_viagem.pdf")

    with open("roteiro_viagem.pdf", "rb") as f:
        st.download_button(
            "📄 Baixar PDF do Roteiro",
            f,
            file_name="roteiro_viagem.pdf",
            mime="application/pdf"
        )