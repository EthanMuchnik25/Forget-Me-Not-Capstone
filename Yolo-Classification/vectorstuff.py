from sentence_transformers import SentenceTransformer

#check for gpu usage
import torch
print(torch.cuda.is_available())

model = SentenceTransformer("dunzhang/stella_en_1.5B_v5", trust_remote_code=True)
# In case you want to reduce the maximum length:
model.max_seq_length = 8192

queries = [
    "game piece",
    "poker chip",
    "pencil",
    "player",
]
# documents = [
#     "As a general guideline, the CDC's average requirement of protein for women ages 19 to 70 is 46 grams per day. But, as you can see from this chart, you'll need to increase that if you're expecting or training for a marathon. Check out the chart below to see how much protein you should be eating each day.",
#     "Definition of summit for English Language Learners. : 1  the highest point of a mountain : the top of a mountain. : 2  the highest level. : 3  a meeting or series of meetings between the leaders of two or more governments.",
# ]

query_embeddings = model.encode(queries, device='cuda')
similarities = model.similarity(query_embeddings, query_embeddings)

# scores = (query_embeddings @ document_embeddings.T) * 100
print(similarities)