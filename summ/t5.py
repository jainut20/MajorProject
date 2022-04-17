import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

text ="""
ABSTRACT DATA TYPES (ADT)
Think of ADT as a black box which hides the inner structure and design of the
data type from the user. w

now the operations allowed on them could be initialised we can define initialise function which initialises the stack to be empty actually we can perform of push operation that is insert an element into the stack we can perform pop operation that is delete an element from the stack we can check is Tak empty all week and Jack is back full so these are the operations which we can define and we can perform on stack these are functions as you can see here we are specified functions but we are not saying anything how they can be implemented we are just specifying them that is called abstract data type we know that what type of elements are allowed and we also know that what operations we can perform but we don't know what is there inside ok think of it as a black box which hides the inner structure and design of the data type from the user we can think of it like it hides all the implementation details from us this is very important that we will understand later there are multiple ways to implement and edit let me tell you this is very important there are multiple ways to implement in edit for example a stack entity can be implemented using arrays or linked lists it should be noted that site itself is a data structure we can implement this data structure using other data structures like a raise or linked list ok so a stat editor which we know is right now skeleton can be implemented using arrays and linked list now the question that immediately arises that why do we even need editors why do we need skeletons why can't we simply implement things your displayed to the user
"""
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')
preprocess_text = text.strip().replace("\n","")
t5_prepared_Text = "summarize: "+preprocess_text
print ("original text preprocessed: \n", preprocess_text)

tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)


# summmarize 
summary_ids = model.generate(tokenized_text,
                                    num_beams=4,
                                    no_repeat_ngram_size=2,
                                    min_length=30,
                                    max_length=100,
                                    early_stopping=True)

output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print ("\n\nSummarized text: \n",output)