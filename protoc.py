from proto_parser import proto_parser
if __name__ == "__main__":
    parser = proto_parser("test_file.proto")
    classes = parser.parse()
    for c in classes:
        print("--------------------------")
        print(f'Class name: {c["name"]}\n')
        print(f'Properties:')
        for p in c["properties"]:
            print(f"{p}\n")
        print(f'Enums:')
        for e in c["enums"]:
            print(f"{e}\n")
        print(f'Subclasses: {c["classes"]}')
        print("--------------------------")
