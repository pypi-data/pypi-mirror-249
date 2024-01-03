from .librarian_base import LibrarianArgFormatter


class LibrarianArgFormatterLLVM(LibrarianArgFormatter):
    def format_input_output_args(self) -> list[str]:
        return ["rc", "%2", "%1"]


class LibrarianArgFormatterGCC(LibrarianArgFormatterLLVM):
    pass

