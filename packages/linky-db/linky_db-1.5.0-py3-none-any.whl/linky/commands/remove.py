import logging

from cliff.command import Command

from linky.actions import remove
from linky.utils import path_utils


class RemoveCommand(Command):
    """
    Permanently removes / deletes a file or folder and all its links.
    Warning: This is a NON-REVERSIBLE action!

    Notice:
    When deleting a directory in a tag folder, this will ONLY remove / delete the
    files and directories WITH the tag. Those without the tag will not be touched.
    To delete an entire folder regardless of tag, use -a/--all
    """

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument("-a", "--all", action="store_true",
                            help="When passed a directory, delete the ENTIRE directory, "
                                 "regardless of tags.")
        parser.add_argument("paths", nargs="+", type=path_utils.abs_path,
                            help="The file or directory to remove")
        return parser

    def take_action(self, parsed_args):
        _log = logging.getLogger("command.remove")
        should_remove_all = parsed_args.all
        for _abs_path in parsed_args.paths:
            if _abs_path.exists():
                try:
                    remove(_abs_path, should_remove_all)
                # pylint:disable=broad-except
                except Exception as exception:
                    _log.error("Couldn't remove '%s': %s",
                               _abs_path, exception,
                               exc_info=True)
            else:
                _log.info("Ignored nonexistent: %s", _abs_path)
