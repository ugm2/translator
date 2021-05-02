from transformers import ProphetNetForConditionalGeneration, XLMProphetNetTokenizer
import os
from summariser import config

print("### Model Loading Script ###")
model = config.DEFAULT_MODEL_PATH

print("# Loading Model...")
m = ProphetNetForConditionalGeneration.from_pretrained(model)
print("# Loading Tokenizer...")
t = XLMProphetNetTokenizer.from_pretrained(model)

print("### Finish ###")