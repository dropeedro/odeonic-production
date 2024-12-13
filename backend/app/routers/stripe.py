from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import stripe
from dotenv import load_dotenv
import os

load_dotenv()

# Inicializar Stripe
stripe.api_key = os.getenv("STRIPE_API_KEY")
print("Stripe API Key:", stripe.api_key)

# Crear router para Stripe
router = APIRouter()

class CreateCheckoutSessionRequest(BaseModel):
    song_id: str  # Agregar un parámetro para identificar la canción que se debe descargar

@router.post("/create-checkout-session")
async def create_checkout_session(request: CreateCheckoutSessionRequest):
    try:
        # Crear la sesión de Stripe con la canción seleccionada
        success_url = f"http://localhost:5173/success?song_id={request.song_id}"
        cancel_url = "http://localhost:5173/cancel"
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'canción',
                    },
                    'unit_amount': 100,  # Precio en centavos (5000 = $50.00)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/download-song")
async def download_song(song_id: str):
    # Define las rutas a los archivos de tus canciones
    songs = {
        "song1": "/Users/pedro/Desktop/odeonic-project/backend/app/static/songs/song1.mp3",
        "song2": "/Users/pedro/Desktop/odeonic-project/backend/app/static/songs/song2.mp3",
        "song3": "/Users/pedro/Desktop/odeonic-project/backend/app/static/songs/song3.mp3",
        "default": "path/to/default.mp3"
    }

    if song_id not in songs:
        raise HTTPException(status_code=404, detail="Song not found")

    file_path = songs[song_id]
    return FileResponse(file_path, media_type='application/octet-stream', filename=f"{song_id}.mp3")
