from abc import ABC, abstractmethod


class LibrarianArgFormatter(ABC):
    @abstractmethod
    def format_input_output_args(self) -> list[str]:
        pass

