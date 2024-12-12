from fasthtml.common import *
from mistralai import Mistral
import os

#import anthropic, os, base64, uvicorn
from dotenv import load_dotenv
load_dotenv()

key =  os.getenv('MISTRAL_API_KEY')
model = "pixtral-12b-2409"
client = Mistral(api_key=key)

app = FastHTML(hdrs=(picolink, Script(open("canvas.js").read(), type="module")))

@app.get("/")
def home():
    return Title('Drawing Demo'), Main(
        H1("Haiku Canvas Demo"),
        Canvas(id="drawingCanvas", width="500", height="500",
               style="border: 1px solid black; background-color: #f0f0f0;"),
        Div("Draw something", id="caption"), cls='container')


@app.post("/process-canvas")
async def process_canvas(image: str):
    image_bytes = await image.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "faça um HAIKU sobre o desenho, e apenas isso."
                    },
                    {
 
                        "type": "image_url",  "image_url": f"data:image/png;base64,{image_base64}"

                    }]}]
            
    chat_response = client.chat.complete(
            model=model,
            messages=messages
            )

    caption = (chat_response.choices[0].message.content.replace("\n", "<br>"))

    #return caption
    return JSONResponse({"caption": caption})

serve()

