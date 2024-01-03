from .librarian_base import LibrarianArgFormatter


class LibrarianArgFormatterMSVC(LibrarianArgFormatter):
    def format_input_output_args(self) -> list[str]:
        return ["/NOLOGO", "/MACHINE:X64", "/WX", "\"%1\"", "/OUT:\"%2\""]

