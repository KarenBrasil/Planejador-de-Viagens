import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import re

# Inicializa para evitar NameError
resposta = None

# 🔑 Configure sua chave API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🔧 Use um dos modelos EXISTENTES
MODEL_NAME = "models/gemini-2.5-pro"
model = genai.GenerativeModel(MODEL_NAME)

# ---------------------------------------------------------
# 📌 Interface Streamlit
# ---------------------------------------------------------

st.title("✈️ Agente Planejador de Viagens")
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

atividade_top = st.text_input("⭐ O que não poderia deixar de fazer:")
restricoes = st.text_area("⚠️ Alguma restrição ou algo que prefere evitar?")
ritmo = st.selectbox(
    "⏱️ Qual o ritmo ideal da viagem?",
    ["Leve (até 2 atividades por dia)", "Moderado (3–4 atividades por dia)", "Intenso (quero aproveitar cada minuto!)"]
)

transporte = st.selectbox(
    "🚗 Como pretende se locomover no destino?",
    ["A pé", "Uber/Taxi", "Carro alugado", "Transporte público"]
)


# ---------------------------------------------------------
# 🔥 GERAR ROTEIRO
# ---------------------------------------------------------

if st.button("Gerar Roteiro"):
    if not destino:
        st.warning("Digite um destino antes!")
    else:
        with st.spinner("Gerando roteiro..."):
            try:

                prompt = f"""
Crie um ROTEIRO COMPLETO para {dias} dias em {destino} para {nome}.

— Estilo da viagem: {estilo}
— Companhia: {companhia}
— Orçamento: {orcamento}
— Ritmo: {ritmo}
— Atividade indispensável: {atividade_top}
— Restrições: {restricoes}
— Transporte: {transporte}

Siga a estrutura obrigatória:

### ✨ Resumão da Viagem
200 a 300 caracteres.

### 🎒 Checklist Pré-Viagem  
- melhor época  
- o que levar  
- cuidados  
- apps úteis  
- transporte ideal  

### 📅 Roteiro Diário (para {dias} dias)
Para cada dia:
- manhã
- tarde
- noite
- horários
- preços
- endereços
- alternativa paga/gratuita

### 🍽️ Gastronomia Local  
### 📸 Pontos Instagramáveis  
### 🌙 Vida Noturna  
### 💡 Dicas de Indispensáveis
### Sua viagem vai ser incrível
                """

                resposta_obj = model.generate_content(prompt)
                resposta = resposta_obj.text

                st.success("Roteiro gerado com sucesso! ✨")
                st.write(resposta)

            except Exception as e:
                st.error(f"Erro ao gerar roteiro: {e}")

# ---------------------------------------------------------
# 📄 GERAR PDF COM REPORTLAB
# ---------------------------------------------------------

def formatar_para_html(texto):
    # Converter títulos
    texto = re.sub(r"### (.*)", r"<br/><b><font size=14>\1</font></b><br/>", texto)
    
    # Converter listas
    texto = texto.replace("* ", "• ")

    # Quebras de linha viram <br/>
    texto = texto.replace("\n", "<br/>")

    return texto

if resposta:
    arquivo_pdf = "roteiro_viagem.pdf"
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=letter)

    styles = getSampleStyleSheet()
    estilo_normal = styles["Normal"]
    estilo_normal.fontSize = 11
    estilo_normal.leading = 15

    elementos = []

    texto_html = formatar_para_html(resposta)
    elementos.append(Paragraph(texto_html, estilo_normal))

    doc.build(elementos)

    with open(arquivo_pdf, "rb") as f:
        st.download_button(
            label="📄 Baixar PDF do Roteiro",
            data=f,
            file_name="roteiro_viagem.pdf",
            mime="application/pdf"
        )