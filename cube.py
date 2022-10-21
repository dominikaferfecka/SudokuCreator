class Cube:
    def __init__(self, value, row, column):
        self._value = value
        self._row = row
        self._column = column
        self._width = 9
        self._selected = False
    
    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self._value = new_value