class Line:
    def __init__(self, str: str, odd: bool = False) -> None:
        self.str = str.rstrip()
        self.depth = self.__calc_depth(str, odd)
        self.sub_content_type = self.__type(str)
        self.odd = odd

    def strip_depth(self) -> str:
        return self.str[self.depth * 2 :]

    def __type(self, str: str) -> str:
        if str.endswith(":"):
            return "list"
        elif str.endswith(": >"):
            return "concatables"
        else:
            return "string"

    def __calc_depth(self, str: str, odd: bool) -> int:
        left_padding = len(str) - len(str.lstrip())
        if left_padding % 2 != 0 and not odd:
            raise Exception(
                f"Uneven number of spaces on left side of line: {left_padding}"
            )

        return int(left_padding / 2)

    def __str__(self) -> str:
        return self.str
