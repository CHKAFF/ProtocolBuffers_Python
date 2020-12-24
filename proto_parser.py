import re


class proto_parser:

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_lines = []
        self.set_file_lines()
        self.classes = []

    def parse(self):
        '''return: `[{"name" : "",\n
            "properties" : [{"modifier" :  "", "type" : "", "name" : ""}],\n
            "enums" : [{"name" : "", "properties" : {}}], \n
            "classes" : []}]`\n
        '''
        while len(self.file_lines) > 1:
            for i in range(len(self.file_lines)):
                line = self.file_lines[i]
                message = re.search("message (.+?) {", line)
                if message is not None:
                    self.file_lines = self.file_lines[i+1:]
                    self.classes.append(self.parse_new_class(message[1]))
                    break
        return self.classes

    def parse_new_class(self, name):
        new_class = {
            "name": name, "properties": [],
            "enums": [], "classes": []
            }
        exit_flag = True

        while exit_flag:
            for j in range(len(self.file_lines)):
                line = self.file_lines[j]
                search = re.search("(\s*)}", line)
                if search is not None:
                    self.file_lines = self.file_lines[j+1:]
                    exit_flag = False
                    break

                search = re.search("message (.+?) {", line)
                if search is not None:
                    self.file_lines = self.file_lines[j+1:]
                    new_subclass = self.parse_new_class(search[1])
                    new_class["classes"].append(new_subclass)
                    break

                search = re.search("enum (.+?) {", line)
                if search is not None:
                    self.file_lines = self.file_lines[j+1:]
                    new_class["enums"].append(self.parse_enum(search[1]))
                    break

                search = re.search("(\S+) (\S+) (\S+) = (.+)", line)
                if search is not None:
                    new_class["properties"].append(
                        {
                            "modifier":  search[1],
                            "type": search[2],
                            "name": search[3]
                        })

        return new_class

    def parse_enum(self, name):
        new_enum = {"name": name, "properties": {}}
        for k in range(len(self.file_lines)):
            line = self.file_lines[k]

            search = re.search("(\s*)}", line)
            if search is not None:
                self.file_lines = self.file_lines[k+1:]
                break

            search = re.search("(\S+) = (\S+)", line)
            if search is not None:
                new_enum["properties"][search[1]] = search[2][:-1]

        return new_enum

    def set_file_lines(self):
        with open(self.file_path, "r") as f:
            for line in f:
                self.file_lines.append(line[:-1])
