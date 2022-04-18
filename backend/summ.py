import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import time

def t5(transcript):
    start_time = time.time()
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    device = torch.device('cpu')
    summary=[]
    for i in transcript:
        text=transcript[i]
        preprocess_text = text.strip().replace("\n","")

        tokenized_text = tokenizer.encode(preprocess_text, max_length=100,return_tensors="pt").to(device)


        # summmarize 
        summary_ids = model.generate(tokenized_text,
                                            num_beams=4,
                                            no_repeat_ngram_size=2,
                                            min_length=30,
                                            max_length=100,
                                            early_stopping=True)

        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summary.append(output)
    print("Total time take by Summarization Algorithm is : %s seconds" % (time.time() - start_time))
    return summary