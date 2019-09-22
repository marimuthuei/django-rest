import math
from rest_framework.exceptions import APIException, ValidationError
from core.settings import FACTORIAl_MAX


def calculator(operator, a, b):
    result = None
    try:
        if operator == "add":
            result = a + b
        elif operator == "sub":
            result = a - b
        elif operator == "mul":
            result = a * b
        elif operator == "div":
            result = a / b
        elif operator == "sqrt":
            result = math.sqrt(a)
        elif operator == "pow":
            result = math.pow(a, b)
        elif operator == "fact":
            if 0 <= a <= FACTORIAl_MAX:
                result = math.factorial(a)
            else:
                raise ValidationError("Factorial number computation limited to 15.")
    except Exception as ex:
        raise APIException("calc error : " + str(ex))
    return result
