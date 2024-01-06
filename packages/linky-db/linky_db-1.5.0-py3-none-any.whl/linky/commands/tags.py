from cliff.command import Command

from linky.actions.tags import get_tags
from linky.config import read_conf
from linky.utils.path_utils import abs_path


class TagsCommand(Command):
    """
    Get tags of a given file
    """

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)

        parser.add_argument("-a", "--absolute",
                            action="store_true",
                            help="Print absolute paths")
        parser.add_argument("paths", nargs="+", type=abs_path)

        return parser

    def take_action(self, parsed_args):
        config = read_conf(parsed_args.paths[0])
        tag_paths = get_tags(config, *parsed_args.paths, relative=not parsed_args.absolute)
        print("\n".join(sorted(str(tag_path) for tag_path in tag_paths)))
