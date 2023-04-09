import sys
import random

NDice = int(sys.argv[1])
NSides = int(sys.argv[2])
LTarget = int(sys.argv[3])
UTarget = int(sys.argv[4])
M = float(sys.argv[5])
NGAMES = int(sys.argv[6])


'''
Given a probability distribution p over the values from 1 to
p.length, choose a random value. Given this is Python, it is safe to use
random.choices().
'''
def chooseFromDist(p):
    # Use random.choices() to choose a value from p
    chosen = random.choices(range(0, len(p)), weights=p)
    return chosen[0]

'''
Simulate the rolling of NDice dice with NSides sides.
'''
def rollDice(NDice, NSides):
    sumOfDice = 0
    for i in range(NDice):
        sumOfDice += random.randint(1, NSides)
    return sumOfDice

'''
Choose the number of dice to roll given the current state of the game.
'''
def chooseDice(X, Y, LoseCount, WinCount, NDice, M):
    K = NDice
    # Initialize K+1 0's
    f = [0 for i in range(K + 1)]
    for J in range(1, K+1):
        # If the denominator is 0, then f[J] = 0.5
        if WinCount[X][Y][J] + LoseCount[X][Y][J] == 0:
            f[J] = 0.5
        else:
            f[J] = (WinCount[X][Y][J] / (WinCount[X][Y][J] + LoseCount[X][Y][J]))
    # Let B be the value of J with the highest value of f[J] (Break Ties randomly)
    B = f.index(max(f))
    # In the event of [0, 0], we want to choose the minimum dice (1), so we set B = 1 if B = 0.
    if (B == 0):
        B = 1
    # Let g be the sum over ALL J that J != B
    g = 0
    for J in range(1, K+1):
        if J != B:
            g += f[J]
    # Let T be the total number of games that have gone through the state X,Y.
    T = 0
    for J in range(1, K+1):
        T = T + WinCount[X][Y][J] + LoseCount[X][Y][J]
    
    # The player rolls B dice with probability:
        # (T*f[B] + M) / (T*f[B] + K*M)
    # For J != B, the player rolls J dice with probability:
        # (1-P[B]) * (T*f[J] + M) / (g*T + (K-1)*M)
    p = [0 for i in range(K+1)]
    # Handle p[B] first since p[J] depends on p[B]
    for J in range(1, K+1):
        if J == B:
            p[B] = (T*f[B] + M) / (T*f[B] + K*M)
        else:
            continue
    # Handle p[J] for J != B
    for J in range(1, K+1):
        if J == B:
            continue
        else:
            p[J] = (1 - p[B]) * ((T*f[J] + M) / (g*T + (K-1)*M))

    # Choose a value from p
    numberOfDiceToRoll = chooseFromDist(p)
    return numberOfDiceToRoll

'''
Simulate the game given the current state.
'''
def playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M):
    for i in range(NGAMES):
        # Initialize the moves of player A and player B to empty
        playerAMoves = []
        playerBMoves = []
        # Initialize the score of player A and player B to 0
        playerAScore = 0
        playerBScore = 0
        # 0 means player A's turn, 1 means player B's turn
        playerTurn = 0
        # Initialize the winner to C (placeholder)
        winner = "C"
        while (playerAScore < LTarget and playerBScore < LTarget):
            # Player A's turn
            if playerTurn == 0:
                # Roll the dice
                numberOfDiceToRoll = chooseDice(playerAScore, playerBScore, LoseCount, WinCount, NDice, M)

                # Update the moves
                playerAMoves.append((playerAScore, playerBScore, numberOfDiceToRoll))

                playerAScore += rollDice(numberOfDiceToRoll, NSides)

                # If player A's score is greater than or equal to LTarget and less than or equal to UTarget, then player A wins
                if playerAScore >= LTarget and playerAScore <= UTarget:
                    winner = "A"
                    break
                # If player A's score is greater than UTarget, then player B wins
                elif playerAScore > UTarget:
                    winner = "B"
                    break
                # If player A's score is less than LTarget, then player A's turn ends and player B's turn begins
                else:
                    playerTurn = 1

            # Player B's turn
            else:
                # Roll the dice
                numberOfDiceToRoll = chooseDice(playerBScore, playerAScore, LoseCount, WinCount, NDice, M)
                
                # Update the moves
                playerBMoves.append((playerBScore, playerAScore, numberOfDiceToRoll))

                playerBScore += rollDice(numberOfDiceToRoll, NSides)

                # If player B's score is greater than or equal to LTarget and less than or equal to UTarget, then player B wins
                if playerBScore >= LTarget and playerBScore <= UTarget:
                    winner = "B"
                    break
                # If player B's score is greater than UTarget, then player A wins
                elif playerBScore > UTarget:
                    winner = "A"
                    break
                # If player B's score is less than LTarget, then player B's turn ends and player A's turn begins
                else:
                    playerTurn = 0
        
        if winner == "A":
            for (x, y, j) in playerAMoves:
                WinCount[x][y][j] += 1
            for (x, y, j) in playerBMoves:
                LoseCount[x][y][j] += 1
        elif winner == "B":
            for (x, y, j) in playerAMoves:
                LoseCount[x][y][j] += 1
            for (x, y, j) in playerBMoves:
                WinCount[x][y][j] += 1
        else:
            pass


'''
Output two LTARGET x LTARGET arrays, one for the best number of dice to roll and one for the probability of winning given making that move.
'''
def extractAnswer(WinCount, LoseCount):
    bestNumberOfDiceToRoll = [[0 for i in range(LTarget)] for j in range(LTarget)]
    probabilityOfWinning = [[0 for i in range(LTarget)] for j in range(LTarget)]

    for i in range(LTarget):
        for j in range(LTarget):
            maxWinCount = 0
            maxWinCountIndex = 0
            for k in range(NDice + 1):
                if WinCount[i][j][k] > maxWinCount:
                    maxWinCount = WinCount[i][j][k]
                    maxWinCountIndex = k
            bestNumberOfDiceToRoll[i][j] = maxWinCountIndex
            if (maxWinCount + LoseCount[i][j][maxWinCountIndex] == 0):
                probabilityOfWinning[i][j] = 0
            else:
                probabilityOfWinning[i][j] = maxWinCount / (maxWinCount + LoseCount[i][j][maxWinCountIndex])

    # Write to file in the same format as the sample output
    with open('output.txt', 'w') as f:
        f.write("PLAY = \n")
        for i in range(LTarget):
            for j in range(LTarget):
                f.write("{:>5d}".format(bestNumberOfDiceToRoll[i][j]))
                f.write("\t")
            f.write("\n")

        f.write("\nPROB = \n")
        for i in range(LTarget):
            for j in range(LTarget):
                f.write("{:>10.4f}".format(probabilityOfWinning[i][j]))
                f.write("\t")
            f.write("\n")

def main():
    WinCount = [[[0 for i in range(NDice + 1)] for j in range(LTarget)] for k in range(LTarget)]
    LoseCount = [[[0 for i in range(NDice + 1)] for j in range(LTarget)] for k in range(LTarget)]

    playGame(NDice, NSides, LTarget, UTarget, LoseCount, WinCount, M)
    extractAnswer(WinCount, LoseCount)

main()
