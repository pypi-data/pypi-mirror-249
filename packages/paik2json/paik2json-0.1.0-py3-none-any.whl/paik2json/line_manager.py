from paik2json.line import Line


class LineManager:
    def __init__(self, raw_data: str, concatables: bool = False):
        self.lines = [Line(line, concatables) for line in raw_data.splitlines() if line]
        self.deepest_depth = max([line.depth for line in self.lines])

    def toString(self) -> str:
        for line in self.lines:
            if line.depth != self.deepest_depth:
                raise Exception(
                    f"lines have different depths. current depth: {line.depth} / deepest depth: {self.deepest_depth}"
                )
        return "".join([line.strip_depth() for line in self.lines])

    def toList(self):
        for line in self.lines:
            if line.depth != self.deepest_depth:
                raise Exception(
                    f"lines have different depths. current depth: {line.depth} / deepest depth: {self.deepest_depth}"
                )
        lst = [str(line).strip() for line in self.lines]
        return lst
