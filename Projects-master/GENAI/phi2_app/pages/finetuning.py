# Install and import the necessary libraries
# !pip install torch peft==0.4.0 bitsandbytes==0.40.2 transformers==4.31.0
#  trl==0.4.7 accelerate einops

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoTokenizer,
    TrainingArguments,
    pipeline,
)
from peft import LoraConfig, PeftModel, prepare_model_for_kbit_training
from trl import SFTTrainer