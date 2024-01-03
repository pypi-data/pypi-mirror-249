# PyStatistics | Factoring






#Imports
from math import sqrt






#Boolean Functions
def checkIfPrime(number: int) -> bool:
    if number == 1: return False
    return len(Factors(number)) == 2




#Other Functions
def Factors(number: int) -> list:
    Factors = iter(([i, number // i] for i in range(1, int(sqrt(number)) + 1) if number % i == 0))
    return sorted(set([int(i) for e in Factors for i in e]))



def PrimeFactors(number: int) -> list:
    PrimeFacts = [1]
    while not checkIfPrime(number):
        number = int(number / PrimeFacts[-1])
        Facts = [int(i) for i in Factors(number) if checkIfPrime(i)]
        PrimeFacts.append(Facts[0])
    
    return PrimeFacts[1:]



def GreatestCommonFactor(Data: list[int] | tuple[int]) -> int:
    Data = [Factors(i) for i in Data]
    FactorAmounts = list(map(len, Data))

    Smallest = Data[FactorAmounts.index(min(FactorAmounts))]
    Data.remove(Smallest)

    return max([Smallest[i] for i in range(len(Smallest)) if [True for D in Data if Smallest[i] in D].count(True) == len(Data)])