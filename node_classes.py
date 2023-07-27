class MachineNode:
  def __init__(self, name, result):
    self.name = name
    self.result = result
    self.materials = []

class ItemNode:
  def __init__(self, name, inputMachine, needed):
    self.name = name
    self.inputMachine = inputMachine
    self.needed = needed
    self.outputMachine = None
    self.quantity = 0