from typing import BinaryIO, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Parameter:
    """
    A parameter name and value to replace a string token in a protocol file with.

    For example, Parameter('foo', 123) would replace '''foo''' with 123 within the contents of a protocol file.
    """
    name: str
    value: object

    @property
    def full_name_b(self) -> bytes:
        """
        The name with quotes, e.g. '''some_string''', as bytes.
        """
        return f"'''{self.name}'''".encode()

    @property
    def value_b(self) -> bytes:
        """
        The value as bytes.
        """
        return f'{self.value}'.encode()


def parameterize_protocol(buffer_in: BinaryIO, buffer_out: BinaryIO, params: Sequence[Parameter]) -> None:
    """
    Replaces parameter tokens with their values in a protocol file binary object as a means of dynamically enabling
    parameters to be injected into an otherwise fixed parameter file.
    :param buffer_in: The protocol file buffer to insert parameters into.
    :param buffer_out: The output protocol file buffer with parameters injected.
    :param params: The parameter names and values to replace.
    """
    if buffer_in is buffer_out:
        raise ValueError("buffer_in and buffer_out can't be the same")

    contents = buffer_in.read()

    for param in params:
        # Check exactly one of each token exists
        count = contents.count(param.full_name_b)
        if count != 1:
            raise ValueError(f'expected 1 occurrence of "{param.full_name_b}", but got {count} occurrences')

        # Replace parameter tokens
        contents = contents.replace(param.full_name_b, param.value_b)

    buffer_out.write(contents)
    buffer_out.seek(0)
