# export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:32
## cuda out of memory errror
## https://huggingface.co/docs/transformers/main/model_doc/phi

# https://blog.gopenai.com/how-to-resolve-runtimeerror-cuda-out-of-memory-d48995452a0
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st
# torch.set_default_device("cuda")
# import gc
# # del variables
# gc.collect()
# import os
# os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb=2048'
#
# torch.cuda.empty_cache()
#
# model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2")
# tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
# inputs = tokenizer('Can you help me write a formal email to a potential business partner proposing a joint venture?', return_tensors="pt", return_attention_mask=False)
#
# outputs = model.generate(**inputs, max_length=30)
# text = tokenizer.batch_decode(outputs)[0]
# print(text)
# st.write(text)

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

@st.cache_resource
def model_load():
    modelpath="microsoft/phi-2"

    model = AutoModelForCausalLM.from_pretrained(
        modelpath,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        # attn_implementation="flash_attention_2",
    )
    tokenizer = AutoTokenizer.from_pretrained(modelpath)
    return model, tokenizer

model,tokenizer=model_load()
prompt=st.text_input("enter the prompt")

# prompt = "The meaning of life is"
# st.write("prompt",prompt)
if prompt:
    input_tokens = tokenizer(prompt, return_tensors="pt").to("cuda")
    output_tokens = model.generate(**input_tokens)
    output = tokenizer.decode(output_tokens[0])

    st.write("output",output)
# print(output)
