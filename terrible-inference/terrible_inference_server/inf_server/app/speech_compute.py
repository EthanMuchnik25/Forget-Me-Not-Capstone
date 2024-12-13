from app.vectorstuffs import  getSimilarityMatrix, getClosestVal

def getMostSimilar(query, listofNames):
    print(f"listofNames: {listofNames}")
    combinedList = [query] + listofNames
    similarities = getSimilarityMatrix(combinedList)
    closestVal = getClosestVal(similarities, combinedList)
    return closestVal