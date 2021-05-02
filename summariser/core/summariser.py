from transformers import XLMProphetNetTokenizer, XLMProphetNetForConditionalGeneration
import torch
import config
import logging
from itertools import chain
from tqdm import tqdm
from typing import List

logging.basicConfig(level=config.LOGGING_LEVEL,
                    format='%(levelname)s:%(message)s')

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i: i + n]

class Summariser:

    def __init__(self,
                 model_path: str = config.DEFAULT_MODEL_PATH,
                 use_cuda: bool = config.GPU,
                 batch_size: int = config.BATCH_SIZE):
        '''
        Constructs all the necessary attributes for the Summariser object.

        Parameters
        ----------
            model_path : str
                path to the summarisation model
            use_cuda : bool
                whether to use CUDA or not (if available)
            batch_size : int
                number of samples passed to the model to predict at once

        '''
        logging.info("Loading model...")
        self.model_path = model_path
        self.use_cuda = use_cuda
        self.batch_size = batch_size
        self.device = "cuda" \
            if torch.cuda.is_available() and self.use_cuda else "cpu"
        self.model = XLMProphetNetForConditionalGeneration.from_pretrained(self.model_path)
        self.tokenizer = XLMProphetNetTokenizer.from_pretrained(self.model_path)
        self.model.to(self.device)
        logging.info(f"Device: {self.device}")
        logging.info(f"Num GPUs Available: {torch.cuda.device_count()}")
        logging.info(f"Model loaded")

    def summarise(self, sentences: List[str], max_length: int = None, min_length: int = None, num_beams: int = 4):
        '''
        Generate summaries from input sentences

        Parameters
        ----------
            sentences : list of str
                list of sentences. Each sentence gets its own summary
        '''
        # Break list into chunks of size self.batch_size
        sentences_chunks = list(chunks(sentences, self.batch_size))

        total_summaries = []
        # Loop over batches of sentences
        for sentences_batch in tqdm(sentences_chunks):
            # Tokenize batch of sentences
            inputs = self.tokenizer.batch_encode_plus(sentences_batch, padding=True, return_tensors='pt')
            # Send inputs to device
            inputs['input_ids'] = inputs['input_ids'].to(self.device)
            inputs['attention_mask'] = inputs['attention_mask'].to(self.device)
            # Generate summary IDs
            args = {
                "input_ids": inputs['input_ids'],
                "attention_mask": inputs['attention_mask'],
                "num_beams": num_beams,
                "early_stopping": True
            }
            if max_length:
                args["max_length"] = max_length
            if min_length:
                args["min_length"] = min_length
            summary_ids = self.model.generate(**args)
            # Decode summary IDs into string sentences
            summaries = self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True)
            total_summaries += summaries
            # Clear cuda cache if needed
            torch.cuda.empty_cache()

        return total_summaries
