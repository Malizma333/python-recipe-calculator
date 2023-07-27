import math, json
from node_classes import MachineNode, ItemNode
from recipe_utilities import getRecipes

class RecipeTree:
  def __init__(self, quantity, recipe_indices, force_raw):
    self.quantity = quantity
    self.recipe_indices = recipe_indices
    self.force_raw = force_raw
    self.remainingItems = {}
    self.materialsList = {}
    self.machineList = []
    self.tree = None

  def generateRecipeTree(self, material):
    root = self.genItemNode(
        name = material,
        inputMachine = None,
        materialsNeeded = self.quantity,
        visited = []
    )

    if material in self.remainingItems:
      del self.remainingItems[material]

    self.tree = root

  def genItemNode(self, name, inputMachine, materialsNeeded, visited):
    node = ItemNode(name, inputMachine, materialsNeeded)

    recipes = getRecipes(name)

    if(len(recipes) == 0):
      self.materialsList[name] = self.materialsList.get(name, 0) + materialsNeeded
      return node
    
    for i in range(len(self.force_raw)):
      if(self.force_raw[i].upper() == name.upper()):
        self.materialsList[name] = self.materialsList.get(name, 0) + materialsNeeded
        return node

    outMachine = None
    chosenRecipeIndex = 0
    if(name.upper() in self.recipe_indices.keys()):
      chosenRecipeIndex = self.recipe_indices[name.upper()] % len(recipes)

    chosenRecipe = recipes[chosenRecipeIndex]

    visited.append(name)

    requiredMaterials = int(chosenRecipe[1])
    materialsProduced = int(math.ceil( materialsNeeded / requiredMaterials ) * requiredMaterials)
    materialsRemaining = materialsProduced - materialsNeeded

    if(materialsRemaining > 0):
      self.remainingItems[name] = self.remainingItems.get(name, 0) + materialsRemaining

    node.quantity = materialsProduced

    outMachine = self.genMachineNode(
        name = chosenRecipe[2],
        result = node,
        recipe = chosenRecipe,
        visited = visited.copy()
    )

    if(outMachine is None):
      return node

    node.outputMachine = outMachine

    return node

  def genMachineNode(self, name, result, recipe, visited):
    node = MachineNode(name, result)

    if(name not in self.machineList):
      self.machineList.append(name)

    materialDict = json.loads(recipe[3].replace("\'", "\""))

    itemNodes = []

    for material, materialCount in materialDict.items():
      if(material in visited):
        return None

      needed = materialCount * int(result.quantity / int(recipe[1]))

      itemNode = self.genItemNode(
          name = material,
          inputMachine = node,
          materialsNeeded = needed,
          visited = visited.copy()
      )

      if(itemNode is None):
        return None

      itemNodes.append(itemNode)

    node.materials.extend(itemNodes)

    return node