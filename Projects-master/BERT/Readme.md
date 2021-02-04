## BERT: It contains stacked with Transformers,
1)	Pretrain to understand language
2)	Fine tune BERT

## Two Phases
### 1)	Pretraining – learns language and Context:
#### Language learning by BERT by training two unsupervised tasks simultaneously 
'''
o	Masked language model (MLM) <br>
o	Next sentence prediction
'''
#### •	Masked language model (MLM)
'''
MLM: Takes input Sentence with random words as filled masks goal is to output masked tokens
Goal: to output masked token
Eg: The [MASK1] brown fox [MASK2] over lazy dog
MASK1=quick
MASK2=jumped
Achieves: Learns bidirectional context
''''
#### •	 Next Sentence Prediction (NSP)
 NSP: Takes two sentence and determines whether second follows first, similar to binary classification
 Eg: Sentence1sentence2 Yes, 1, True
     Sentence1Sentence3 No, 0, False


### 2)	Finetune BERT : Its required to trained for particular tasked 

  #### In Question Answering 
  Input: Question and Passage 
  Output : Answer to fully connected layer


Input
Set of two words where some words are masked

Initial Embedding is constructed through 3 vectors 
1)	Token Embedding: Pre-Trained Word embedding (Word piece embedding trained on 30k words vocabulary)
2)	Segment Embedding: Sentence embedded into vectors
3)	Position Embedding: Position of word into sentence 
Note: Segment and position embedding temporal ordering.

Output 

Binary C(NSP) and word vectors
Note: Word vectors same size and all generated simultaneously
Word vectorfully connected layer Softmax activation [0-1] where neurons equal to total no of words in vocab Comparing with actual labels i.e. one hot encoded using Cross Entropy loss  
'''
Summary: 
1)	We pretrained BERT language model using mask language modelling and Next sentence prediction
2)	Every word token embedding using word piece, Segment Embedding, position embedding 
3)	Passed into BERT which outputs word vectors for masked language model and NSP as Binary value.
4)	Word vectors converted into distribution to train using Cross Entropy Loss.
5)	We performed supervised training depending task we want to perform
Note: Squad large Note: BERT large 340M Parameters, BERT Base 110 M Parameters 
'''


### BERT: Stack of transformer Encoder 

#### ENCODER
Input: 
Word Embedding
Words converted to vector but different words have different meanings in sentence.

Position Embedding: vector gives context based on position: Sin and Cosine function.

X=word vector+ pos vector 

Encoder Block:
X goes encoder block i.e.  Multi headed attention and feed forward layer.
Multi headed attention: How relevant word is relevant to other words in same sentence.
Feed Forward net: Are use to transform attention vector

#### DECODER 
Input: X=Embedding layer +position embedding 

Decoder Block:  It contains 3 main block 

1)	Multi head attention: How relevant word is relevant to other words in same sentence.
Captures contextual relationship between words
2)	Encoder Decoder Block: Attention vector and vector from Encoder block as input: 
In Language translation: Each vector represents relationships with other words in both languages. 
3)	Feed Forward Layer
4)	Linear Layer: It used to expand dimensions to no of words in output vocabulary, 
 


### BERT MODELS
•	BERT
•	distilBERT
•	ALBERT
•	RoBERTa
•	XLNet
•	XLM
•	FlauBERT

