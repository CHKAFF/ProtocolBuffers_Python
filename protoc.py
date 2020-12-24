from proto_parser import proto_parser
from converter import converter
import sys
import args_parser

def main(args):
    parser = proto_parser(args.file)
    classes_data = [x for x in parser.parse() if x["name"] in args.classes or args.classes == []]
    con = converter(classes_data)
    if args.output_file == "":
        file_name = args.file[:-5] + "py"
    else:
        file_name = args.output_file
    with open(file_name, "w") as out_file:
        out_file.write(con.run())

if __name__ == "__main__":
    main(args_parser.args_parser().get_args())
