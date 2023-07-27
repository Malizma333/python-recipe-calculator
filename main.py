import json
from os import system
from recipe_tree import RecipeTree
from visualizer import printRecipe, printMaterials
from retrieve_recipes import isValidItem
from constants import settingsJsonPath

def main():
  with open(settingsJsonPath, 'r') as settings_json:
    settings = json.load(settings_json)

  while(True):
    system('CLS')

    item = input("Enter the id of an item: ").upper()

    while(not isValidItem(item)):
      print("Invalid item!")
      item = input("Enter the id of an item: ").upper()
    
    quantity = input("Enter quantity (default 1): ")
    quantityN = 1

    try:
      if(len(quantity.strip()) != 0):
        quantityN = int(quantity)
    except:
      print("Invalid quantity, defaulting to 1...")
      quantityN = 1

    recipeTree = RecipeTree(
      quantity = quantityN,
      recipe_indices = settings['recipe_index'],
      force_raw = settings['force_raw_material']
    )
    
    recipeTree.generateRecipeTree(item)

    if(settings['print_recipe']): printRecipe(recipeTree.tree)
    if(settings['print_materials']): printMaterials(recipeTree.materialsList, "Material List")
    if(settings['print_machines']): printMaterials(recipeTree.machineList, "Machine List")
    if(settings['print_remaining']): printMaterials(recipeTree.remainingItems, "Remaining List")

    exit = input("\nPress enter to restart or type 'e' to exit...\n")

    if(exit.lower() == 'e'):
      break

main()