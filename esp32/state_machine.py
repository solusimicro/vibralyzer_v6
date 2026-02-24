# state_machine.py

class StateMachine:
    def __init__(self):
        self.state = "BOOT"

    def set(self, new_state):
        self.state = new_state
        print("STATE ->", self.state)

    def get(self):
        return self.state
