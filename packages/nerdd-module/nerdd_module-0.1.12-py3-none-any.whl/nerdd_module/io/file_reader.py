from .reader import Reader
import os

class FileReader(Reader):
    def __init__(self, inner_content_reader : Reader):
        super().__init__()
        self.inner_content_reader = inner_content_reader

    def read(self, input):
        if not isinstance(input, str) or not os.path.exists(input):
            raise TypeError("input must be a valid filename")
        
        for entry in self.inner_content_reader.read(open(input, "rb")):
            yield entry._replace(source=input)
    
    def _input_format(self):
        return self.inner_content_reader.input_format
    
    def __repr__(self) :
        return f"FileReader(inner_content_reader={self.inner_content_reader})"