import argparse

class args_parser:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='protoc')
        self.parser.add_argument(dest='file', action='store',
                    help='proto file path')
        self.parser.add_argument('-c', dest='classes', action='store',
                                    nargs='*', default=[], help='classes')
        self.parser.add_argument('-o', dest='output_file', action='store',
                                     default="", help='output file')
    
    def get_args(self):
        return self.parser.parse_args()