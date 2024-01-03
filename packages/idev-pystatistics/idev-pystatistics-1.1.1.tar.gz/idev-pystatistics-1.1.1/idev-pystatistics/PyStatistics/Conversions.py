#PyStatistics | Conversion Functions






#Imports
from NumberTypes import *





#Functions
def float_to_fraction(number: float) -> Fraction:
    number = str(number)

    splitter = number.index('.')

    leftNumber = number[:splitter]
    rightNumber = number[splitter + 1:]

    denominator = 10 ** len(rightNumber)
    numerator = denominator * int(leftNumber) + int(rightNumber)

    return Fraction(numerator, denominator).simplify()



def int_to_fraction(number: int) -> Fraction:
    return float_to_fraction(float(number))



def decimal_to_fraction(number: Decimal) -> Fraction:
    return float_to_fraction(number.stringForm)



def weightedNumber_to_fraction(number: WeightedNumber) -> Fraction: 
    return decimal_to_fraction(number.floatForm)



def float_to_decimal(number: float) -> Decimal:
    number = str(number).split('.')
    return Decimal(number[0], number[1])



def int_to_decimal(number: int) -> Decimal:
    return Decimal(number, 0)



def fraction_to_decimal(number: Fraction) -> Decimal:
    number = str(number.floatForm).split('.')
    return Decimal(number[0], number[1])



def weightedNumber_to_decimal(number: WeightedNumber) -> Decimal:
    number = str(number.floatForm).split('.')
    return Decimal(number[0], number[1])



def float_to_weightedNumber(number: float, weight: int | float) -> WeightedNumber:
    if type(weight) == int: weight /= 100.0
    elif type(weight) == float:
        if weight > 1: weight /= 100.
    if weight > 1: return None

    return WeightedNumber(round((number / weight), 2), weight)



def int_to_weightedNumber(number: int, weight: int | float) -> WeightedNumber:
    return float_to_weightedNumber(float(number), weight)



def decimal_to_weightedNumber(number: Decimal, weight: int | float) -> WeightedNumber:
    return float_to_weightedNumber(number.floatForm, weight)



def fraction_to_weightedNumber(number: Fraction, weight: int | float) -> WeightedNumber:
    return decimal_to_weightedNumber(fraction_to_decimal(number), weight)