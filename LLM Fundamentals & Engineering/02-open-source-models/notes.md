What is hugging face?
github for the llms. open source libraries that everyone can use.

What is pytorch & tensor flow?

What is the difference between running a open souce modal using ollama and hugging face?

ollama: takes care of everything we just have to write the commmands
hugging face: you can run the modal by yourself, you’ll have the source code.

first library is hugging face hub? this is a python library to connect to the hugging face hub. and login through code and connect to model.

second library is dataset. it allows you to manipulate a large amount of data in an effective way.

third library: transformers, i want this specific model i want the code for it i want to run it i want to train it i wannt to do anything with it.

peft: parameter efficient fine tuning: 

what is lora and qlora.

TRL: transformer reinforcement learning library.

Accelerate: distribute model across multiple gpus.


----------

What is google colab, run a jupyter notebook in the cloud with a powerful runtime. Also it allows you to colaborate. 

you can have a google colab with 15GB gpu nvidia tesla t4 for fee?

GPU go obselete, gpu that are hot today they will not be hot a year after. if you buy one you’ll stuck with it.


You can connect a google colab with a hugging face account.

Include the code examples of google colab of running stable diffusion free modals from hugging face and generating images, multiple examples, also include refiners.

Also include the examples of generating audio.

Generate the image using black forest lab.

When you’re running A100 Nvidia GPU, make sure to terminate the gpu.


--------------------

Two levels of hugging face api

pipelines (higher level apis to carry out standard tasks incredibly quickly)
Tokenizers and model (Lower level api to provide the most power and control)

Hugging face pipe lines out of the box inference tasks

 - Sentiment analysis, classifier, named entity recognition, question and answering, summarizing, translation.

also include all of the examples with sample outputs in this notebook explained. ‘https://colab.research.google.com/drive/1aMaEw8A56xs0bRM4lu8z7ou18jqyybGm?usp=sharing’

-------------------------------

What is a token?

what is a special token?

What is a tokenizer. what is encode and decode?

contains a vocab that can include special tokens to signal information to the LLM, like start of prompt. (what is this)

incldue the tokenizer examples with output for these models.

 - llama 3.1, phi 4, deepseek 3.1, qwen 2.5 coder.

Include the examples present in this page ‘https://colab.research.google.com/drive/1WD6Y2N7ctQi1X9wa6rpkg8UfyA4iSVuz?usp=sharing’

-------------

Dive deeper into the quantizations?

what is 16 bit and 32 bit? nums set during training time.

Example of a dimmer switch.

include the examples present in this page ‘https://colab.research.google.com/drive/1hhR9Z-yiqjUe7pJjVQw4c74z_V3VchLy?usp=sharing’






inside llama decoder layers, attention, and why non linearity matters.

explainn this object


LlamaForCausalLM(
 (model): LlamaModel(
 (embed_tokens): Embedding(128256, 4096)
 (layers): ModuleList(
 (0-31): 32 x LlamaDecoderLayer(
 (self_attn): LlamaSdpaAttention(
 (q_proj): Linear(in_features=4096, out_features=4096, bias=False)
 (k_proj): Linear(in_features=4096, out_features=1024, bias=False)
 (v_proj): Linear(in_features=4096, out_features=1024, bias=False)
 (o_proj): Linear(in_features=4096, out_features=4096, bias=False)
 (rotary_emb): LlamaRotaryEmbedding()
 )
 (mlp): LlamaMLP(
 (gate_proj): Linear(in_features=4096, out_features=14336, bias=False)
 (up_proj): Linear(in_features=4096, out_features=14336, bias=False)
 (down_proj): Linear(in_features=14336, out_features=4096, bias=False)
 (act_fn): SiLU()
 )
 (input_layernorm): LlamaRMSNorm((4096,), eps=1e-05)
 (post_attention_layernorm): LlamaRMSNorm((4096,), eps=1e-05)
 )
 )
 (norm): LlamaRMSNorm((4096,), eps=1e-05)
 )
 (lm_head): Linear(in_features=4096, out_features=128256, bias=False)
)










explain the code and each and every thing in this colab notebook.

https://colab.research.google.com/drive/1KSMxOCprsl1QRpt_Rq0UqCAyMtPqDQYx?usp=sharing

