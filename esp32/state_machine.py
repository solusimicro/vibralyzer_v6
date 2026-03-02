class StateMachine:

    def __init__(self):
        self.state = "BOOT"

    def set(self, s):
        self.state = s
        print("STATE ->", s)

    def get(self):
        return self.state
