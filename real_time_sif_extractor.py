
class RealTimeSifExtractor:

    def __init__(self):
        pass

    def tooLoud(self, data):
        return any(data > 0.7)
