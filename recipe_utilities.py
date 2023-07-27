import csv, difflib
from constants import csvPath

def getRecipes(result):
  recipeList = []
  with open(csvPath, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
      if row[0] != result:
        continue
      recipeList.append(row)
  return recipeList

def isValidItem(item):
  if(item is None):
    return False
  
  recipeList = getRecipes(item)

  if(recipeList is None or len(recipeList) == 0):
    return False
  
  return True

def getSimilarItems(item):
  if(item is None):
    return False
  
  recipes = []

  with open(csvPath, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
      recipes.append(row[0])
  
  matches = difflib.get_close_matches(item, recipes)
  
  return matches