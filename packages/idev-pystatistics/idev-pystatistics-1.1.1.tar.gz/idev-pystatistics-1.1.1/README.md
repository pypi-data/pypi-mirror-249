# **PyStatistics**
A [**python**](https://www.python.org) collection of classes and functions to help with numbers along with collections of numbers i.e., **statistics**.
<br />
<br />
​<br />
# Installation
With `git` [GitHub](https://github.com):
```
git clone https://github.com/IrtsaDevelopment/PyStatistics.git
```
With `pip` [PyPi](https://pypi.org/project/idev-pystatistics/)
```
pip install idev-pystatistics
```
<br />
<br />
<br />
<br />
<br />

# Usage
To import:
```py
from PyStatics.NumberTypes import *
from PyStatics.Conversions import *
from PyStatics.Factoring import *
from PyStatics.Lists import *
```
<br />
<br />
<br />
<br />

## NumberTypes
Includes classes defining extra number types of **Decimal**, **WeightedNumber**, and **Fraction**.
<br />
<br />

### Decimal
```py
decimal = Decimal(1, 4)
decimal = Decimal(1, "04")
decimal = Decimal("1", 4)
decimal = Decimal("1", "342")

# A Decimal has two main parts, the integeral and fractional (left and right side of the decimal point).
# Note that when creating a Decimal, the inputs can accept integers, or strings to allow for leading zeros before a decimal.
```
```py
decimal = Decimal(1, 3412)
print(decimal)
# Printing the Decimal as is will print off the decimal as expected.
# Result: 1.3412


decimal = Decimal(1, "0043284238472923798")
print(decimal)
# This can be expanded more to allow for more decimal places to be displayed.
# Result: 1.0043284238472923798
```
<br />

The **Decimal** class also has the following properties:
```py
decimal.integeral
decimal.fractional
# Corresponding parts of the Decimal.

decimal.stringForm
# Will return a string version of the Decimal.

decimal.floatForm
# Will return a float version of the Decimal, note that some accuracy may be lost when doing so.
```
<br />
<br />

### WeightedNumber
```py
weightedNumber = WeightedNumber(100, 10)
weightedNumber = WeightedNumber(100.0, 10.0)
weightedNumber = WeightedNumber(100, 0.1)

# A WeightedNumber has two main parts, the number and the weight as a percentage (both represented as an integer or float).
# Note that when creating a WeightedNumber, the weight can either be between 0-1 or 0-100 and either will be recognized as a valid weight percentage.
```
```py
weightedNumber = WeightedNumber(100, 10)
print(weightedNumber)
# Printing the WeightedNumber as is will print off the number and it's weight percentage.
# Result: 100 - 10.0%

weightedNumber = WeightedNumber(10, 0.1)
print(weightedNumber)
# As expected, both values are treated as 10%
# Result: 100 - 10.0%
```
<br />

The **WeightedClass** class also has the following properties:
```py
weightedNumber.number
weightedNumber.weight
# Corresponding number and weight of the number in their given form.

weightedNumber.weightType
# Will return 'whole' or 'decimal' depending on the value range and type of the given weight.

weightedNumber.percentForm
# Will return the weight as a percentage.

weightedNumber.stringForm
# Will return a string version of the WeightedNumber.

weightedNumber.floatForm
# Will return a float version of the WeightedNumber (the number multiplied by the weight).
```
<br />
<br />

### Fraction
```py
fraction = Fraction(10, 100)
fraction = Fraction(100, 10)

# A Fraction has two main parts, the numerator and the denominator (both represented as an integer).
```
```py
fraction = Fraction(10, 100)
print(fraction)
# Printing the Fraction as is will print off a simplified fraction representation of the numbers.
# Result: 1/10
```
<br />

The **Fraction** class also has the following properties:
```py
fraction.numerator
fraction.denominator
# Corresponding numerator and denominator of the Fraction.

fraction.stringForm
# Will return a string version of the Fraction.

fraction.floatForm
# Will return a float version of the Fraction (the numerator divided by the denominator).
```
The **Fraction** class also has the following function(s):
```py
fraction.simplify()
# Will return the Fraction simplified to have the lowest possible numerator and denominator and still be equal.

fraction = Fraction(120, 140)
print(fraction.simplify())
# Result: 6/7
```
<br />
<br />

### Matrix
```py
matrix = Matrix([1, 3, 2], [1, 3, 4], [7, 3, 1])

# A Matrix has is comprised of columns and rows, each row of the column is a separate argument in the form of a list.
# Note that Matrix division currently only supports Matrices of 2x2 or 3x3.
```
```py
matrix = Matrix([1, 3, 2], [1, 3, 4], [7, 3, 1])
print(matrix)
# Printing the Matrix as is will print off the matrix in a grid format.
# Result:
# 1 3 2
# 1 3 4
# 7 3 1
```
<br />

The **Matrix** class also has the following properties:
```py
matrix.matrix
# A list containing the rows of the matrix (list of lists).

matrix.dimensions
# Will return a tuple of the dimensions of the matrix (rows, columns).
```
<br />
<br />
<br />
<br />

Each of the classes supports the ability to have arithmetic operations be performed.
```py
fractionA = Fraction(1, 2)
fractionB = Fraction(1, 5)


print(fractionA + fractionB)
# Result: 7/10

print(fractionA - fractionB)
# Result: 3/10

print(fractionA * fractionB)
# Result: 1/10

print(fractionA / fractionB)
# Result: 5/2
```
```py
decimalA = Decimal(1, 5)
decimalB = Decimal(2, 8)


print(decimalA + decimalB)
# Result: 4.3

print(decimalA - decimalB)
# Result: -1.7

print(decimalA * decimalB)
# Result: 4.2

print(decimalA / decimalB)
# Result: 0.5357142857142857
```
```py
weightedNumberA = WeightedNumber(10, 30)
weightedNumberB = WeightedNumber(10, 70)


print(weightedNumberA + weightedNumberB)
# Result: 10.0

print(weightedNumberA - weightedNumberB)
# Result: 4.0

print(weightedNumberA * weightedNumberB)
# Result: 21.0

print(weightedNumberA / weightedNumberB)
# Result: 0.42857142857142855
```
```py
matrixA = Matrix([10, 9], [8, 8])
matrixB = Matrix([2, 1], [3, 2])


print(matrixA + matrixB)
# Result:
# 12 10
# 11 10

print(matrixA - matrixB)
# Result:
# 8 8
# 5 6

print(matrixA * matrixB)
# Result:
# 47 28
# 40 24

print(matrixA / matrixB)
# Result:
# 11.0 8.0
# 8.0 8.0
```
When performing mixed class arithmetic operations, the preceding class type will be the output type.
```py
fraction = Fraction(1, 3)
decimal = Decimal(1, 4242)
weightedNumber = WeightedNumber(100, 30)


print(fraction + decimal)
# Result: 26363/15000
# Fraction

print(decimal + weightedNumber)
# Result: 31.4242
# Decimal

print(weightedNumber + fraction)
# Result: 30.33
# WeightedNumber
```
Current python int and float classes are supported in mixed class arithmetic operations.
```py
fraction = Fraction(1, 3)
decimal = Decimal(1, 4242)
weightedNumber = WeightedNumber(100, 30)


print(2.0 - decimal)
# Result: 0.5758

print(fraction - 1)
# Result: -2/3

print(weightedNumber + 3)
# Result: 33.0
```
Matrices are supported in mixed class arithmetic operations, though the Matrix has to be the proceeding type and the arithmetic will be applied to each value in the Matrix.
```py
matrix = Matrix([1, 3], [4, 9])
fraction = Fraction(1, 2)
decimal = Decimal(1, 45)
weightedNumber = WeightedNumber(100, 30)


print(matrix + decimal)
# Result:
# 2.45 4.45
# 5.45 10.45

print(matrix - fraction)
# Result:
# 0.5 2.5
# 3.5 8.5

print(matrix * weightedNumber)
# Result:
# 30.0 90.0
# 120.0 270.0

print(matrix - 3)
# Result:
# -2 0
# 1 6
```
<br />
<br />
<br />
<br />

## Conversions
Includes functions dedicated to converting between different NumberTypes including current Int and Float types.
<br />
<br />

### Functions
```py
float_to_fraction(number: float) -> Fraction
# Will convert a Float value to a Fraction value.

int_to_fraction(number: int) -> Fraction
# Will convert an Int value to a Fraction value.

decimal_to_fraction(number: Decimal) -> Fraction
# Will convert a Decimal value to a Fraction value.

weightedNumber_to_fraction(number: WeightedNumber) -> Fraction
# Will convert a WeightedNumber value to a Fraction value.


float_to_decimal(number: float) -> Decimal
# Will convert a Float value to a Decimal value.

int_to_decimal(number: int) -> Decimal
# Will convert an Int value to a Decimal value.

fraction_to_decimal(number: Fraction) -> Decimal
# Will convert a Fraction value to a Decimal value.

weightedNumber_to_decimal(number: WeightedNumber) -> Decimal
# Will convert a WeightedNumber value to a Decimal value.


float_to_weightedNumber(number: float, weight: int | float) -> WeightedNumber
# Will convert a Float value with a provided weight value to a WeightedNumber value.

int_to_weightedNumber(number: int, weight: int | float) -> WeightedNumber:
# Will convert a Int value with a provided weight value to a WeightedNumber value.

decimal_to_weightedNumber(number: Decimal, weight: int | float) -> WeightedNumber
# Will convert a Decimal value with a provided weight value to a WeightedNumber value.

fraction_to_weightedNumber(number: Fraction, weight: int | float) -> WeightedNumber
# Will convert a Fraction value with a provided weight value to a WeightedNumber value.
```
```py
print(float_to_fraction(0.3123))
# Result: 3123/10000
# Fraction

print(fraction_to_decimal(Fraction(3123, 10000)))
# Result: 0.31
# Decimal
# Note: Slight accuracy lost.

print(weightedNumber_to_decimal(WeightedNumber(10, 0.1)))
# Result: 1.0
# Decimal
```
<br />
<br />
<br />
<br />

## Factoring
Includes functions dedicated to factoring numbers.
<br />
<br />

### Functions
```py
checkIfPrime(number: int) -> bool
# A boolean function that checks if an integer number is a prime number or not.
# True if is, False otherwise.

Factors(number: int) -> list
# Returns a list of the factors of an integer number.

PrimeFactors(number: int) -> list
# Returns a list of the prime factorization of an integer number.

GreatestCommonFactor(Data: list[int] | tuple[int]) -> int
# Returns the GCF (Greatest Common Factor) from a list (or tuple) of integers.
```
```py
print(checkIfPrime(12323232131))
# Result: False

print(Factors(12323232131))
# Result: [1, 7, 29, 203, 60705577, 424939039, 1760461733, 12323232131]

print(PrimeFactors(12323232131))
# Result: [7, 29, 60705577]

print(GreatestCommonFactor([42387132, 4238, 232342]))
# Result: 2
```
<br />
<br />
<br />
<br />

## Lists
Includes functions dedicated to traditional statics such as **mean**, **median**, and **mode**.
<br />
<br />

### Functions
```py
Mode(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> int | float
# Returns the mode (most common number) of a given list (or tuple) of numbers.

Median(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> int | float
# Returns the median (middle of the list when ordered) of a given list (or tuple) of numbers.

Mean(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the mean (average of the summed numbers) of a given list (or tuple) of numbers.

QuartileFirst(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the Q1 (first quartile) (the middle of the first half of the list when ordered [~25%]) of a given list (or tuple) of numbers.

QuartileThird(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the Q3 (third quartile) (the middle of the second half of the list when ordered [~75%]) of a given list (or tuple) of numbers.

InterQuartileRange(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the IQR (inter quartile range) (the difference between the third and first quartiles) of a given list (or tuple) of numbers.

Range(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the range (the difference between the highest and lowest value) of a given list (or tuple) of numbers.

Outliers(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list
# Returns the outliers (any number falling outside of a specific range determined by the different of the Q1 and 1.5 times the IQR and the sum of Q3 and 1.5 times the IQR) of a given list (or tuple) of numbers.

Variance(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the variance (the spread between the numbers) of a given list (or tuple) of numbers.

StandardDeviation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the SD (standard deviation) (the amount of variation relative to the mean) of a given list (or tuple) of numbers.

MeanAbsoluteDeviation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the MAD (mean absolute deviation) (the average distance between each number and the mean) of a given list (or tuple) of numbers.

AverageIncrease(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the AI (average increase) (the average amount each value is increased) of a given list (or tuple) of numbers.

AverageMultiplication(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float
# Returns the AM (average multiplication) (the average amount each value is multiplied) of a given list (or tuple) of numbers.

AverageIncreaseInterpolation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list
# Returns an interpolation (estimating other potential values of a list of numbers) of a given list (or tuple) of numbers by using the AI (average increase) of the list (or tuple).

AverageMultiplicationInterpolation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list
# Returns an interpolation (estimating other potential values of a list of numbers) of a given list (or tuple) of numbers by using the AM (average multiplication) of the list (or tuple).

PointIncreaseInterpolation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list
# Returns an interpolation (estimating other potential values of a list of numbers) of a given list (or tuple) of numbers by using the mean of each number and the number after.

PointMultiplicationInterpolation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list
# Returns an interpolation (estimating other potential values of a list of numbers) of a given list (or tuple) of numbers by using the AM (average multiplication) of each number and the number after.
```
```py
Data = [43, 321, 912, 213, 213, 9, 34843]


print(Mode(Data))
# Result: 213

print(Median(Data))
# Result: 213

print(Mean(Data))
# Result: 52220.0

print(QuartileFirst(Data))
# Result: 119.5

print(QuartileThird(Data))
# Result: 9072.25

print(InterQuartileRange(Data))
# 8952.75

print(Range(Data))
# 34834.0

print(Outliers(Data))
# Result: [34843]

print(Variance(Data))
# Result: 170696185.67

print(StandardDeviation(Data))
# Result: 13065.08

print(MeanAbsoluteDeviation(Data))
# Result: 8463.14

print(AverageIncrease(Data))
# Result: 5800.0

print(AverageMultiplication(Data))
# Result: 647.17

print(AverageIncreaseInterpolation(Data))
# Result: [43.0, 2943.0, 321.0, 3221.0, 912.0, 3812.0, 213.0, 3113.0, 213.0, 3113.0, 9.0, 2909.0, 34843.0]

print(AverageMultiplicationInterpolation(Data))
# Result: [43.0, 13914.15, 321.0, 103870.78, 912.0, 295109.52, 213.0, 68923.6, 213.0, 68923.6, 9.0, 2912.26, 34843.0]

print(PointIncreaseInterpolation(Data))
# Result: [43.0, 182.0, 321.0, 616.5, 912.0, 562.5, 213.0, 213.0, 213.0, 111.0, 9.0, 17426.0, 34843.0]

print(PointMultiplicationInterpolation(Data))
# Result: [43.0, 160.5, 321.0, 456.0, 912.0, 106.5, 213.0, 106.5, 213.0, 4.5, 9.0, 17421.5, 34843.0]
```
​
<br />
<br />
<br />
<br />
# Additional Notes
Accuracy may be lost at times when converting between number formats.
