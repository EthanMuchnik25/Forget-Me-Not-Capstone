from sentence_transformers import SentenceTransformer

#check for gpu usage
import torch
import requests
from app.config import Config 
print(torch.cuda.is_available())

def doRemoteInfs(query, wordList):
    # print(format_texts_lists(texts_lists))

    data = {"query": query, "wordList": wordList}
    
    response = requests.post(Config.VECTOR_COSINE_REMOTE_ENDPOINT, json=data)

    if response.status_code == 200:
        # request was successful
        return response.json()
    else:
        return None


def getModelName():
    if Config.VECTOR_COSINE == "HEAVY-COMPUTE":
        return "dunzhang/stella_en_1.5B_v5"
    elif Config.VECTOR_COSINE == "LIGHT-COMPUTE":
        return "dunzhang/stella_en_400M_v5"
    else:
        return "dunzhang/stella_en_1.5B_v5"

def getMostSimilar(query, listofNames):
    print(f"listofNames: {listofNames}")
    combinedList = [query] + listofNames
    similarities = getSimilarityMatrix(combinedList)
    closestVal = getClosestVal(similarities, combinedList)
    return closestVal

    

def getSimilarityMatrix(listofNames):

    model = SentenceTransformer(getModelName())
    # In case you want to reduce the maximum length:
    model.max_seq_length = 8192

    queries = listofNames

    query_embeddings = model.encode(queries, device='cuda')
    similarities = model.similarity(query_embeddings, query_embeddings)

    # convert tensor to numpy array
    similarities = similarities.cpu().detach().numpy()
    print(similarities)

    # scores = (query_embeddings @ document_embeddings.T) * 100
    return similarities

def getClosestVal(similarityMatrix, listofNames):
    # Get closest value to the first value in the list
    closestVal = similarityMatrix[0][1]
    closestIndex = 1
    for i in range(2, len(listofNames)):
        if similarityMatrix[0][i] > closestVal:
            closestVal = similarityMatrix[0][i]
            closestIndex = i

    if closestVal < Config.SIMILARITY_THRESHOLD:
        return "None"

    return listofNames[closestIndex]

if __name__ == "__main__":
    # getSimilarityMatrix(["game piece", "poker chip", "pencil", "player"])
    closestVal = getMostSimilar("game piece", ["potato", "pencil", "pencils"])

    print(closestVal)