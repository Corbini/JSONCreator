

class Call:
    call = lambda parents, name, value, command: print(parents,',', name, ': ', command, '->', value)
    
    @classmethod
    def change_call(cls, func):
        cls.call = func
