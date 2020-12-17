import sys

args = sys.argv

tftOdds = [[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0.75, 0.25, 0, 0, 0], 
	[0.55, 0.3, 0.15, 0, 0], [0.45, 0.3, 0.2, 0.05, 0], [0.3, 0.35, 0.25, 0.1, 0],
	[0.19, 0.35, 0.3, 0.15, 0.01], [0.14, 0.2, 0.35, 0.25, 0.06],
	[0.1, 0.15, 0.3, 0.3, 0.15]]

poolSize = [29, 22, 18, 12, 10]

numUnits = [13 * poolSize[0], 13 * poolSize[1], 13 * poolSize[2], 11 * poolSize[3], 8 * poolSize[4]]

def calculate(unitsTaken, numLevelTaken, levelOfUnit, level, gold):
	numRolls = gold // 2
	odds = tftOdds[level-1][levelOfUnit-1]

	pctOfLevel = float(poolSize[levelOfUnit-1] - unitsTaken) / float(numUnits[levelOfUnit-1] - numLevelTaken)
	
	#kinda Inaccurate
	oddsPerShop = 1 - pow(1-(odds * pctOfLevel), 5)

	print(1-pow(1-oddsPerShop, numRolls))
	return 1-pow(1-oddsPerShop, numRolls)

calculate(int(args[1]), int(args[2]), int(args[3]), int(args[4]), int(args[5]))