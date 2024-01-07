from rosh.filters import RoshFilter

import os
from prompt_toolkit.completion import PathCompleter

class RoshTeeCommand(RoshFilter):
    description = 'save a copy of the output to file'

    def __init__(self, rosh):
        def _get_paths_cb():
            return os.getcwd()

        completer = PathCompleter(get_paths=_get_paths_cb, expanduser=True)
        super().__init__(rosh, completer=completer)

    def handler(self, cmd, *args):
        print(args)

is_rosh_filter = False
rosh_filter = RoshTeeCommand
