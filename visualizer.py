class Format:
    end = '\033[0m'
    underline = '\033[4m'
    sixteenStacks = ['bucket', 'egg', 'honey bottle', 'ender pearl', 'armor stand']

    def stackableItem(name, quantity):
      stackShift = 6
      stackAnd = 63
      stacks = ''
      remainder = ''

      if(name.lower() in Format.sixteenStacks):
        stackShift = 4
        stackAnd = 15
      
      if(quantity & stackAnd != 0):
        remainder = str(quantity & stackAnd)
      
      if(quantity >> stackShift != 0):
        stacks = str(quantity >> stackShift) + ' x ' + str(stackAnd + 1)
      
      if(stacks != '' and remainder != ''):
        remainder = ' + ' + remainder

      return stacks + remainder

def printMaterials(objects, title):
  if(not bool(objects)):
    return
  
  print(Format.underline + "\n" + title + Format.end)
  if(isinstance(objects, list)):
    for item in objects:
      itemName = ' '.join(word.capitalize() for word in item.replace('_', ' ').split())
      print(itemName)
  else:
    for material, quantity in objects.items():
      matName = ' '.join(word.capitalize() for word in material.replace('_', ' ').split())
      print(matName, ':', Format.stackableItem(material, quantity))

def printRecipe(recipeTree):
  print(Format.underline + "\nRecipeTree" + Format.end)
  printRecipeRec(recipeTree)

def printRecipeRec(result):
  if(result is None):
    return

  if(result.outputMachine is None):
    return

  for material in result.outputMachine.materials:
    printRecipeRec(material)

  print()

  for material in result.outputMachine.materials:
    print(material.name)

  print('v')
  print(result.outputMachine.name)
  print('v')
  print(result.name)