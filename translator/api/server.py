from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from easynmt import EasyNMT

app = FastAPI()
# translator = EasyNMT('m2m_100_1.2B', device='cpu') #  Facebook's
translator = EasyNMT('opus-mt', device='cpu')

first_example = \
"Según el portal oficial de la organización, Microsoft tiene la intención de terminar formalmente sus operaciones contra Windows después del 14 de enero de 2020"
second_example = \
"根据该组织的官方门户网站，微软公司打算在2020年1月14日之后正式终止对Windows "

class Payload(BaseModel):
    sentences: List[str] = Field(title="Sentences to translate",
                                 example=[first_example, second_example])
    target_lang: str = Field(title="Target Language",
                             example="en")

class Translations(BaseModel):
    translations: List[str] = Field(None, title="Translations")

async def translate_async(sentences, target_lang):
    return translator.translate(sentences, target_lang=target_lang)

@app.post("/translate", response_model=Translations, status_code=200, name="translate")
async def translate(payload: Payload):
    translations = await translate_async(payload.sentences, payload.target_lang)
    translations = Translations(translations=translations)
    return translations
