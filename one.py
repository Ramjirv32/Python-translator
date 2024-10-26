from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from googletrans import Translator, LANGUAGES

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

translator = Translator()

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        # Validate language codes
        if request.source_lang != "auto" and request.source_lang not in LANGUAGES:
            raise HTTPException(status_code=400, detail="Invalid source language code")
        if request.target_lang not in LANGUAGES:
            raise HTTPException(status_code=400, detail="Invalid target language code")

        # Perform translation
        translation = translator.translate(
            request.text,
            src=request.source_lang,
            dest=request.target_lang
        )

        return TranslationResponse(
            original_text=request.text,
            translated_text=translation.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
