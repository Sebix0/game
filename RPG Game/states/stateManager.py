

class StateManager:
  def __init__(self, startState):
    self.state = startState
    self.prevState = None

  def setState(self, state):
    self.prevState = self.state
    self.state = state

  def getState(self):
    return self.state

  def getPrevState(self):
    return self.prevState
  
  def back(self):
    temp = self.state
    self.state = self.prevState
    self.prevState = temp
  
class State:
  def __init__(self, stateManager):
    self.stateManager = stateManager

  def logic(self):
    pass

  def eventHandler(self, event):
    pass

  def render(self, win, offset):
    pass

  def load(self):
    pass