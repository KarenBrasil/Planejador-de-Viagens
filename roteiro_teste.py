import google.generativeai as genai

genai.configure(api_key="AIzaSyBG8Ui2Iq_a4m8_1WtTLykyiDXizSUuffs")

try:
    model = genai.GenerativeModel("gemini-1.5-pro")
    resposta = model.generate_content("Diga apenas: OK, funcionando.")
    print("\nRESPOSTA DO GEMINI →", resposta.text)
except Exception as e:
    print("\nERRO ENCONTRADO:", e)
