import streamlit as st
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

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

### 🍽️ Gastronomia Imperdível  
### 📸 Pontos Instagramáveis  
### 🌙 Vida Noturna  
### 💡 Dicas de Ouro  
### Finalização motivadora
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

if resposta:

    pdf_filename = "roteiro_viagem.pdf"

    styles = getSampleStyleSheet()
    style = styles["Normal"]

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    # Adiciona texto com suporte a UTF-8
    for linha in resposta.split("\n"):
        story.append(Paragraph(linha.replace("\n", "<br/>"), style))

    doc.build(story)

    with open(pdf_filename, "rb") as f:
        st.download_button(
            "📄 Baixar PDF do Roteiro",
            f,
            file_name=pdf_filename,
            mime="application/pdf"
        )
