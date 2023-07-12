from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Replicate
from dotenv import load_dotenv
import urllib.request
import base64
from fastapi import UploadFile, File
from starlette.responses import RedirectResponse
from pydantic import BaseModel

# FastAPI scaffolding
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

# Initialize replicate endpoints
r8_llm =  Replicate(model="replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b")
r8_musicgen = Replicate(model="pollinations/music-gen:297edd2fef3473ff62277678dce50b32148c5ffc5c1fadac98bc288f5050a6f8")
r8_music_to_music_video = Replicate(model="pollinations/lucid-sonic-dreams-xl:14334f96bf01f6f96d74f00d07dc90f8fc64e7d568ee1231deb7a8b556a9dd87")
r8_conditioned_musicgen = Replicate(model="joehoover/musicgen:ba9bdc5a86f60525ba23590a03ae1e407b9a40f4a318a85af85748d641e6659f")

# LangChain initialization
enrich_music_prompt = """
Based on the following information from the user, please craft a great description of a sound/music sample that is more detailed and creative than the input text: 
{text}
"""

prompt_template = PromptTemplate(
    template=enrich_music_prompt,
    input_variables=['text'],
)
chain = LLMChain(
    llm=r8_llm,
    prompt=prompt_template,
)

#==============================================================================
# FastAPI endpoints
#==============================================================================

@app.post('/enrich-music-description')
async def enrich_music_description(text: str) -> str:
    """
    Creative enrichment of music description.

    Returns the enriched text.
    """    
    enriched_text = chain.run(text=text)
    return enriched_text

class R8MusicGenPayload(BaseModel):
    type: str
    title: str
    format: str

@app.post('/pipeline-text-to-enrich-to-music')
async def pipeline_text_to_enrich_to_music(text: str) -> str:
    """
    Creative enrichment of music description.
    Converts the enriched text to a sound sample.

    Returns the URL of the generatic music.
    """    
    enriched_text = chain.run(text=text)
    return r8_musicgen(enriched_text)

@app.post('/text-to-music')
async def text_to_music(text: str):
    """
    Converts the text to a sound sample.

    Returns the URL of the generatic music.
    """    
    return {"sample_url": r8_musicgen(text)}

@app.post('/text-plus-music-to-music')
async def text_x_music_to_music(
    prompt: str,
    melody: UploadFile,
    duration: int=30,
    continuation: bool=False,
    temperature: float = 1.0

):
    """
    Given a melody and a prompt, generate a music sample in line with the melody.
    Options to either be inspired by or continue the melody.
    """
    # new_prompt = chain.run(text=prompt)
    data_split = melody.split('base64,')
    encoded_melody = data_split[1]
    # melody = base64.b64decode(encoded_data)
    payload = {
        "prompt": prompt,
        "melody": encoded_melody,
        "duration": duration,
        "continuation": continuation,
        "temperature": temperature,
        "model_version": "melody",
    }
    new_sample = r8_musicgen(**payload)
    return {
        "sample_url": new_sample,
        "prompt": prompt,
    }

@app.post('/music-to-music-video')
async def music_to_music_video(
    model_type: str,
    audio_file: bytes,
    fps: int = 25,
    pulse_react: int = 60,
    pulse_react_to: str = "harmonic",
    motion_react: int = 60,
    motion_react_to: str = "harmonic",
    motion_randomnes: int = 50,
    truncation: int = 40,
    batch_size: int = 20
    ):
    return {
        "video_url": r8_music_to_music_video(
            model_type=model_type,
            audio_file=audio_file,
            fps=fps,
            pulse_react=pulse_react,
            pulse_react_to=pulse_react_to,
            motion_react=motion_react,
            motion_react_to=motion_react_to,
            motion_randomnes=motion_randomnes,
            truncation=truncation,
            batch_size=batch_size
        )
    }