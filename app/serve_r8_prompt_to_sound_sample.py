from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Replicate
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".secrets")
# FASTAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

# LANGCHAIN
r8_llm =  Replicate(model="replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b")
r8_musicgen = Replicate(model="pollinations/music-gen:297edd2fef3473ff62277678dce50b32148c5ffc5c1fadac98bc288f5050a6f8")

pr_music_prompt = """
Based on the following information from the user, please craft a great description of a sound/music sample that is more detailed and creative than the input text: 
{text}
"""

prompt_template = PromptTemplate(
    template=pr_music_prompt,
    input_variables=['text'],
)
chain = LLMChain(
    llm=r8_llm,
    prompt=prompt_template,
)

@app.post('/prompt-to-sample')
async def prompt_to_sample(text: str):
    prompt = chain.run(text=text)
    return {
        "sample_url": r8_musicgen(prompt),
        "prompt": prompt
    }

@app.post('/text-to-sample')
async def text_to_sample(text: str):
    return {"sample_url": r8_musicgen(text)}

@app.post('/sample-to-music-video')
async def sample_to_music_video(sample_url: str):
    return {"music_video_url": r8_musicgen(sample_url)}