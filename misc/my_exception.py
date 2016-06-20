"""define my exceptions
"""

class DebugStop(Exception):
        def __init__(self,message):
            self.message = "Stop for debuging\n"+message
            pass
        def __str__(self):
            return self.message