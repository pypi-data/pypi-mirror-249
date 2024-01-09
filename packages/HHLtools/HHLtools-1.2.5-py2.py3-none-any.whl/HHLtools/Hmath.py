from HHLtools.Herror import *

class Function:
    def __init__(self, expression: str, variable: str):
        if type(expression) != str:
            error(TypeError, f"the expression must be a string, not '{str(type(expression))[7:-1]}'")
        if type(variable) != str:
            error(TypeError, f"the variable must be a string, not '{str(type(variable))[7:-1]}'")
        self.__expression = expression
        self.__var = variable

    def evaluate(self, value: int | float):
        if type(value) not in (int, float):
            error(TypeError, f"the value must be an integer, or a real number, not '{str(type(value))[7:-1]}'")
        expression = self.__expression.replace(self.__var, str(value))
        return eval(expression)

    def gradient(self, accuracy: float, value: int | float):
        if type(value) not in (int, float):
            error(TypeError, f"the value must be an integer, or a real number, not '{str(type(value))[7:-1]}'")
        if type(accuracy) != float:
            error(TypeError, f"the acuuracy must be a real number, not '{str(type(value))[7:-1]}'")
        x1 = value
        x2 = value + 10 ** -accuracy
        y1 = self.evaluate(x1)
        y2 = self.evaluate(x2)
        res = (y2 - y1) / (x2 - x1)
        return round(res, 1) if res - int(res) > 0.999 or res - int(res) < 0.001 else round(res, 3)



class Vector:
    def __init__(self, dimensions:list):
        """
        only support two-dimensional and three-dimensional vectors
        :param dimensions: the components of the vector in i, j(, k) directions
        """
        if len(dimensions) != 2 and len(dimensions) != 3:
            error(DimensionError, f'expected 2 or 3 dimensions, got {len(dimensions)}')
        self.dimensions = dimensions

    def __repr__(self):
        return f'Vector({self.dimensions})'

    def __len__(self):
        return len(self.dimensions)

    def __eq__(self, other):
        return self.dimensions == other.dimensions

    def __add__(self, other):
        if type(other) != Vector:
            error(TypeError, f"unsupported operand type(s) for +: 'Vector' and {str(type(other))[7:-1]}")
        if len(self) != len(other):
            error(DimensionError, f'unsupported operand dimension(s) for +: Vectors of different dimensions')
        res = [self.dimensions[i] + other.dimensions[i] for i in range(len(self))]
        return Vector(res)

    def __sub__(self, other):
        if type(other) != Vector:
            error(TypeError, f"unsupported operand type(s) for -: 'Vector' and {str(type(other))[7:-1]}")
        if len(self) != len(other):
            error(DimensionError, f"unsupported operand dimension(s) for -: Vectors of different dimensions")
        res = [self.dimensions[i] - other.dimensions[i] for i in range(len(self))]
        return Vector(res)

    def __mul__(self, other):
        if type(other) == int:
            return Vector([other * i for i in self.dimensions])
        elif type(other) == Vector:
            if len(self) != len(other):
                error(DimensionError, f"unsupported operand dimension(s) for *: Vectors of different dimensions")
            return sum([self.dimensions[i] * other.dimensions[i] for i in range(len(self))])
        else:
            error(TypeError, f"unsupported operand type(s) for *: 'Vector' and {str(type(other))[7:-1]}")

    def __rmul__(self, other):
        if type(other) == int:
            return Vector([other * i for i in self.dimensions])
        elif type(other) == Vector:
            if len(self) != len(other):
                error(DimensionError, f"unsupported operand dimension(s) for *: Vectors of different dimensions")
            return sum([self.dimensions[i] * other.dimensions[i] for i in range(len(self))])
        else:
            error(TypeError, f"unsupported operand type(s) for *: {str(type(other))[7:-1]} and 'Vector'")

    def __abs__(self):
        return sum([i**2 for i in self.dimensions])**(1/2)

    def __matmul__(self, other):
        if type(other) != Vector:
            error(TypeError, f"unsupported operand type(s) for @: 'Vector' and {str(type(other))[7:-1]}")
        if len(self.dimensions) != 3 or len(other.dimensions) != 3:
            error(DimensionError, f"unsupported operand dimension(s) for @: Not 3 dimension Vector(s)")
        x = self.dimensions[1] * other.dimensions[2] - self.dimensions[2] * other.dimensions[1]
        y = self.dimensions[2] * other.dimensions[0] - self.dimensions[0] * other.dimensions[2]
        z = self.dimensions[0] * other.dimensions[1] - self.dimensions[1] * other.dimensions[0]
        return Vector([x,y,z])

class Line:
    _chars = []
    def __init__(self, position:Vector, direction:Vector, scalar:str):
        if len(position) != 3:
            error(DimensionError, f'expected 3 dimensions, got {len(position)}')
        if len(direction) != 3:
            error(DimensionError, f'expected 3 dimensions, got {len(direction)}')
        chars = self.__class__._chars
        if scalar in chars:
            error(NameError, f"duplicated scalar symbol {scalar}")
        chars.append(scalar)
        self.position = position
        self.direction = direction
        self.scalar = scalar

    def __repr__(self):
        pos = self.position.dimensions
        di = self.direction.dimensions
        return f'({pos[0] if pos[0] != 1 else ""}i+' \
               f'{pos[1] if pos[1] != 1 else ""}j+' \
               f'{pos[2] if pos[2] != 1 else ""}k) + ' \
               f'{self.scalar}' \
               f'({di[0] if di[0] != 1 else ""}i+' \
               f'{di[1] if di[1] != 1 else ""}j+' \
               f'{di[2] if di[2] != 1 else ""}k)'


p = Vector([1,2,3])
d = Vector([1,2,3])
l1 = Line(p, d, 'r')

print(l1)

