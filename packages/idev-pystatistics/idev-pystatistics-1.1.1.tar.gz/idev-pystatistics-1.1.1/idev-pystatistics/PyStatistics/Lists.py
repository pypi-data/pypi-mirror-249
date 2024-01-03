# PyStatistics | List Functions






#Imports
from NumberTypes import *






#Private Functions
def __ConvertData(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]):
    return [i.floatForm if type(i) in [WeightedNumber, Fraction] else i for i in Data]




#Public Functions
def Mode(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> int | float:
    Data = __ConvertData(Data)
    Data = {i: Data.count(i) for i in Data}

    return max(Data, key = Data.get)



def Median(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> int | float:
    Data = __ConvertData(Data)

    if len(Data) == 0: return None
    if len(Data) == 1: return Data[0]

    Data = sorted(Data)
    x = int(len(Data) / 2)

    if len(Data) % 2 == 0: return round(((Data[x - 1] + Data[x]) / 2.0), 2)
    return Data[x]



def Mean(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    Data = __ConvertData(Data)
    return round((sum(Data) / len(Data)), 2)



def QuartileFirst(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    Data = sorted(__ConvertData(Data))
	
    x = int(len(Data) / 2)
    return Mean(Data[:(x + 1)])



def QuartileThird(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    Data = sorted(__ConvertData(Data))
	
    x = int(len(Data) / 2)
    return Mean(Data[x:])



def InterQuartileRange(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    q1 = QuartileFirst(Data)
    q3 = QuartileThird(Data)
	
    return q3 - q1



def Range(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
	return float(max(Data) - min(Data))



def Outliers(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list:
    Data = __ConvertData(Data)

    iqr = InterQuartileRange(Data)

    upperBound = QuartileThird(Data) + (1.5 * iqr)
    lowerBound = QuartileFirst(Data) - (1.5 * iqr)

    return [i for i in Data if i > upperBound or i < lowerBound]



def Variance(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    Data = __ConvertData(Data)
    mean = Mean(Data)
    return round((sum([((i - mean) ** 2) for i in Data]) / (len(Data) - 1)), 2)



def StandardDeviation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    Data = __ConvertData(Data)
    variance = Variance(Data)
    return round((variance ** 0.5), 2)



def MeanAbsoluteDeviation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    Data = __ConvertData(Data)
    mean = Mean(Data)
    return round((sum([abs(i - mean) for i in Data]) / len(Data)), 2)



def AverageIncrease(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    Data = __ConvertData(Data)
    Data = [(Data[i + 1] - Data[i]) for i in range(len(Data) - 1)]
    return round((sum(Data) / len(Data)), 2)



def AverageMultiplication(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> float:
    Data = __ConvertData(Data)
    Data = [(Data[i + 1] / Data[i]) for i in range(len(Data) - 1)]
    return round((sum(Data) / len(Data)), 2)



def AverageIncreaseInterpolation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list:
    Data = __ConvertData(Data)
    
    ai = AverageIncrease(Data) / 2.0

    Data = [[Data[i], Data[i] + ai] for i in range(len(Data))]
    return [float(i) for e in Data for i in e][:-1]



def AverageMultiplicationInterpolation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list:
    Data = __ConvertData(Data)

    am = AverageMultiplication(Data) / 2.0
    Data = [[Data[i], Data[i] * am] for i in range(len(Data))]
    return [round(float(i), 2) for e in Data for i in e][:-1]



def PointIncreaseInterpolation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list:
    Data = __ConvertData(Data) + [0]

    Differences = [((Data[i + 1] - Data[i]) / 2) for i in range(len(Data) - 1)]
    
    Data = [[Data[i], Data[i] + Differences[i]] for i in range(len(Differences))]
    return [round(float(i), 2) for e in Data for i in e][:-1]



def PointMultiplicationInterpolation(Data: list[WeightedNumber, Fraction, Decimal, int, float] | tuple[WeightedNumber, Fraction, Decimal, int, float]) -> list:
    Data = __ConvertData(Data) + [0]

    Multipliers = [((Data[i + 1] / Data[i]) / 2) for i in range(len(Data) - 1)]

    Data = [[Data[i], Data[i] * Multipliers[i]] for i in range(len(Multipliers))]
    return [round(float(i), 2) for e in Data for i in e][:-1]