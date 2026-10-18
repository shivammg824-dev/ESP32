from fastapi import FastAPI, File, UploadFile
import google.generativeai as genai
import os

app = FastAPI()

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/")
def home():
    return {"status": "Krishak Robot Hands-Free Server is Running!"}

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    try:
        audio_path = "temp_audio.wav"
        with open(audio_path, "wb") as buffer:
            buffer.write(await file.read())

        # Gemini AI ko audio file bhejein jo wake-word aur query dono analyze karega
        audio_file = genai.upload_file(audio_path)
        prompt = "Aap Krishak Robot hain. Pehle check karein ki kya user ne 'Krishak Robot' bola hai. Agar haan, toh jo aage sawal pucha gaya hai uska chhota, saaf aur madadgaar jawab Hindi ya Hinglish mein dijiye."
        response = model.generate_content([audio_file, prompt])
        
        reply_text = response.text
        print(f"AI Reply: {reply_text}")

        os.remove(audio_path)
        return {"status": "success", "reply": reply_text}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}