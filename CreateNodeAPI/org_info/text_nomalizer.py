import unicodedata

class TextNormalizer:

    def __init__(self):
        pass

    def normalize(self, text):
        return unicodedata.normalize('NFKC', text)
