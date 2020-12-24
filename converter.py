class converter:

    def __init__(self, classes):
        self.classes = classes
        self.level = 0
        self.code = ""
        self.default_values = {'string' : 'str', 'int32' : "int", 'int64' : 'int'}

    def run(self):
        for c in self.classes:
            self.add_class(c)
        return self.code

    def add_class(self, c, is_subclass = False):
        self.add_line("import pickle\n")
        self.add_empty_line()
        self.add_line(f"class {c['name']}:\n")
        self.up_indent()
        if len(c["properties"]) != 0:
            self.add_properties(c["properties"])
            self.add_empty_line()

        if not is_subclass:
            self.add_serialization()
            self.add_deserialization()

        for enum in c["enums"]:
            self.add_enum(enum)
            self.add_empty_line()
        
        for subc in c['classes']:
            self.add_class(subc, True)
            self.add_empty_line()
        
        self.down_indent()

    def add_properties(self, properties):
        self.add_line("def __init__(self):\n")
        self.up_indent()
        for p in properties:
            if p['modifier'] == "repeated":
                self.add_line( f"self.{p['name']} = ()\n")
            else:
                self.add_line(f"self.{p['name']} = {self.get_default_value(p['type'])}\n")
        self.down_indent()
        
    def add_enum(self, enum):
        self.add_line(f"class {enum['name']}:\n")
        self.up_indent()
        for p in enum["properties"]:
            self.add_line(f"{p} = {enum['properties'][p]}\n")
        self.down_indent()

    def add_serialization(self):
        self.add_line("def serialization(self):\n")
        self.up_indent()
        self.add_line("return pickle.dumps(self)\n")
        self.down_indent()
        self.add_empty_line()
    
    def add_deserialization(self):
        self.add_line("def deserialization(self, data):\n")
        self.up_indent()
        self.add_line("return pickle.loads(data)\n")
        self.down_indent()
        self.add_empty_line()


    def get_default_value(self, value_type):
        if value_type in self.default_values:
            return f"{self.default_values[value_type]}()"
        return f"{value_type}()"

    def add_line(self, string):
        self.code += self.indent() + string

    def add_empty_line(self):
        self.code += "\n"

    def indent(self):
        return "\t" * self.level
    
    def up_indent(self):
        self.level += 1

    def down_indent(self):
        if self.level > 0:
            self.level -= 1