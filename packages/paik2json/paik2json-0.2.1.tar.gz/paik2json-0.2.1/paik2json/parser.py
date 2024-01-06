import copy
from paik2json.line_manager import LineManager


class Parser:
    def __init__(self, text, hook=lambda x: x):
        self.line_manager = LineManager(text)
        self.hook = hook
        self.table = self.__to_table()

    def __to_table(self):
        table = [[None] * (self.line_manager.deepest_depth + 1)]
        for index, line in enumerate(self.line_manager.lines):
            right_empties_count = self.line_manager.deepest_depth - line.depth
            table[index][line.depth] = self.hook(line.strip_depth())
            table[index] = table[index][: line.depth + 1] + (
                [None] * right_empties_count
            )
            if index < len(self.line_manager.lines) - 1:
                table.append(copy.deepcopy(table[index]))
        return table

    def parse(self):
        json = {}
        for i in range(self.line_manager.deepest_depth + 1):
            for raw in self.table:
                if raw[i] is None:
                    continue

                upper = json
                for index in range(i + 1):
                    if index < i:
                        upper = upper[raw[index]]
                    else:
                        upper[raw[index]] = {}

        return self.__convert_leaf_node(json)

    def __convert_leaf_node(self, dictionary):
        keys = dictionary.keys()

        flag = False
        for key in keys:
            if dictionary[key] == {}:
                flag = True
            else:
                flag = False
                break

        if flag:
            dictionary = list(keys)
            return dictionary

        for key in keys:
            if dictionary[key] != {}:
                dictionary[key] = self.__convert_leaf_node(dictionary[key])
            else:
                dictionary[key] = []

        return dictionary
