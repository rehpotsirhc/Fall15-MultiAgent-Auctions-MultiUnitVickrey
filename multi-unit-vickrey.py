__author__ = 'chris'
import random
import pandas
import locale
from operator import itemgetter
pandas.set_option('display.width', 1000)
locale.setlocale( locale.LC_ALL, '' )


VALUE_SMALLEST_DENOM = 5
NUM_DENOMS = 10
NUM_ITEMS = 30


# used for converting a bidders index to a name
# 65 means bidder 0 is named A, bidder 1 is named B, etc.
BIDDER_NAME_CHAR_OFFSET = 65










def doAuctions(numOfAuctions):
    global numOfBidders

    # 3D matrix of auction results for each auction
    # auctions[0][0] holds the following information for bidder 0 at auction 0:
    # number of items won, price paid/item, utility (price paid/item - clearing price)
    # so auctions[0][0][0] holds the number of items won by bidder 0 in auction 0
    # auctions[0][0][1] holds the price  paid/item by bidder 0 in auction 0
    # auctions[0][0][2] holds the utility gained by bidder 0 in auctio 0
    global auctions

    # 2D matrix that holds the averages of auctions
    global auctionsAvg

    # matrix of bidders and their desired quantity at each possible denomination
    # bidders[0][1] holds the desired quantity of bidder 0 at denomination 2 (denominations start at 1 but array is 0 based)
    global bidders


    global avgClearingPrice


    auctions = []
    auctionsAvg = []
    bidders = []
    avgClearingPrice = 0

    # pre-init auctions and bidders matrices
    numOfBidders = initBidders()
    initAuctions(numOfAuctions, numOfBidders)

    print('\n')
    print('Quantity: ' + str(NUM_ITEMS))
    print('Denomination: ' + locale.currency(VALUE_SMALLEST_DENOM))
    print('Price Range: ' + locale.currency(VALUE_SMALLEST_DENOM) + '-' + locale.currency(VALUE_SMALLEST_DENOM * NUM_DENOMS))
    for a in range(0, numOfAuctions):
        createBids()
        #printBidderMatrix('Auction ' + str(a + 1) + ' (Bidders and Prices)')
        clearingDenom = determineClearingDenom(-1)
        avgClearingPrice += (clearingDenom * VALUE_SMALLEST_DENOM)

        for b in range(0, numOfBidders):
            cd = determineClearingDenom(b)
            auctions[a][b][1] = locale.currency( cd * VALUE_SMALLEST_DENOM)
            auctions[a][b][2] = locale.currency(VALUE_SMALLEST_DENOM * (clearingDenom - cd))

        determineNumItemsWon(a, clearingDenom)

        print('\n')
        printAuctionResults(auctions[a], 'Auction ' + str(a + 1) + ' (Results)')
        print('\n')
        print('Clearing price:')
        print(locale.currency(clearingDenom * VALUE_SMALLEST_DENOM ))
        print('\n\n\n')



    avgAuctions()
    avgClearingPrice /= numOfAuctions
    print('Avg Clearing price: ' + locale.currency(avgClearingPrice))
    printAuctionResults(auctionsAvg, 'Average Auction Results')



def initAuctions(numOfAuctions, numOfBidders):
    for a in range(0, numOfAuctions):
        auctions.append([])
        for b in range(0, numOfBidders):
            auctions[a].append([])
            for i in range(0, 3):
                auctions[a][b].append(0)

    for b in range(0, numOfBidders):
         auctionsAvg.append([])
         for i in range(0, 3):
             auctionsAvg[b].append(0)


def initBidders():
    numBidders = 0
    for nameQuant in bidderTypes:
        numBidders += nameQuant[0]

    for b in range(0, numBidders):
        bidders.append([])
        for d in range(0, NUM_DENOMS):
            bidders[b].append(0)

    return numBidders


def createBids():
    for i in range(0, len(bidderTypes)):
        nameQuant = bidderTypes[i]
        indices = bidderTypeIndexToBidderIndices(i)
        if nameQuant[1] == 'Random':
            createRandomBidders(indices)
        elif nameQuant[1] == 'Slow':
            createSlowBidders(indices)
        elif nameQuant[1] == 'Quick':
            createQuickBidders(indices)
        elif nameQuant[1] == 'MediumSpeed':
            createMediumBidders(indices)
        elif nameQuant[1] == 'High':
            createAlwaysHighBidders(indices)
        elif nameQuant[1] == 'Low':
            createAlwaysLowBidders(indices)
        elif nameQuant[1] == 'Medium':
            createAlwaysMediumBidders(indices)


def createRandomBidders(indices):


    for b in indices:
        current = NUM_ITEMS
        for d in range(0, NUM_DENOMS):
            step = random.randint(0, current - random.randint(0, current))
            lowerBound = current - step
            if lowerBound < 0:
                lowerBound = 0
            current = random.randint(lowerBound, current)
            bidders[b][d] = current



def createAlwaysHighBidders(indices):
    for b in indices:
        for d in range(0, NUM_DENOMS):
            bidders[b][d] = NUM_ITEMS

def createAlwaysMediumBidders(indices):
    for b in indices:
        for d in range(0, NUM_DENOMS):
            bidders[b][d] = NUM_ITEMS / 2


def createAlwaysLowBidders(indices):
    for b in indices:
        for d in range(0, NUM_DENOMS):
            bidders[b][d] = NUM_ITEMS / (NUM_ITEMS - NUM_ITEMS / 2)

def createMediumBidders(indices):
    createBidderOfSpeed(indices, 3)


def createSlowBidders(indices):
    createBidderOfSpeed(indices, 2)


def createQuickBidders(indices):
    createBidderOfSpeed(indices, 6)


def createBidderOfSpeed(indices, speed):
    if speed > NUM_DENOMS:
        speed = NUM_DENOMS

    evenDecrementAmount = speed * (NUM_ITEMS / NUM_DENOMS)

    for b in indices:
        current = NUM_ITEMS
        for d in range(0, NUM_DENOMS):
            decrementAmount = evenDecrementAmount - random.randint(0, evenDecrementAmount)
            lowbound= current - decrementAmount
            if lowbound < 0:
                lowbound = 0
            current = random.randint(lowbound, current)
            bidders[b][d] = current


def bidderTypeIndexToBidderIndices(bidderTypeIndex):
    numOfMyType = bidderTypes[bidderTypeIndex][0]
    sum = 0
    for counter in range(bidderTypeIndex - 1, -1, -1):
        sum += bidderTypes[counter][0]

    indices = []
    for count in range(0, numOfMyType):
        indices.append(sum + count)

    return indices


def bidderIndexToBidderTypeIndex(bidderIndex):

    lastSum = 0
    sum = 0
    for i in range(0, len(bidderTypes)):
        sum += bidderTypes[i][0]

        if bidderIndex >= lastSum and bidderIndex < sum:
            return bidderTypes[i][1]

        lastSum = sum



def determineNumItemsWon(auctionIndex, clearingPrice):
    bidderItemQtyAtCP = {}
    totalNumOfItems = NUM_ITEMS

    for b in range(0, numOfBidders):
        bidderItemQtyAtCP[b] =bidders[b][clearingPrice - 1]


    bidderItemQtyAtCPDescending = sorted(bidderItemQtyAtCP.items(), key=itemgetter(1), reverse=True)

    for kv in bidderItemQtyAtCPDescending:
        b = kv[0]
        qty= kv[1]
        totalNumOfItems -= qty
        if totalNumOfItems < 0:
            qty += totalNumOfItems
        auctions[auctionIndex][b][0] = qty
        if totalNumOfItems <= 0:
            break



def determineClearingDenom(skipBidderIndex):
    clearingDenom = 0
    for d in range(NUM_DENOMS - 1, -1, -1):
        sum = 0
        for b in range(0, numOfBidders):
            if skipBidderIndex != b:
                sum += bidders[b][d]

        if sum >= NUM_ITEMS:
            clearingDenom = d + 1
            break

    return clearingDenom



def printAuctionResults(auction, title):

    columnTitles = ['# items won | ', 'price/item paid | ', 'utility']
    bidderTitles = []
    for b in range(0, numOfBidders):
        bidderTitles.append('Bidder ' + chr(BIDDER_NAME_CHAR_OFFSET + b) + ' (' +bidderIndexToBidderTypeIndex(b) + ')')

    print2DArray(auction, title, bidderTitles, columnTitles)

def printBidderMatrix(title):

    denomTitles = []
    bidderTitles = []
    for b in range(0, numOfBidders):
        bidderTitles.append('Bidder ' + chr(BIDDER_NAME_CHAR_OFFSET + b) + ' (' +bidderIndexToBidderTypeIndex(b) + ') | ')

    for d in range(0, NUM_DENOMS):
        denom = d + 1
        denomTitles.append('Price: ' + locale.currency(denom * VALUE_SMALLEST_DENOM) + "  (" + str(denom)+")")


    print2DArray(list(zip(*bidders)), title, denomTitles, bidderTitles)


def print2DArray(twoDArray, title, rowTitles, columnTitles):
    print(title)

    print(pandas.DataFrame(twoDArray, rowTitles , columnTitles))



def avgAuctions():

    numOfAuctions = len(auctions)
    for a in range(0,  numOfAuctions):
        for b in range(0, numOfBidders):
            auctionsAvg[b][0] += auctions[a][b][0]
            auctionsAvg[b][1] += locale.atof(auctions[a][b][1].strip("$"))
            auctionsAvg[b][2] += locale.atof(auctions[a][b][2].strip("$"))

    for b in range(0, numOfBidders):
        auctionsAvg[b][0] /=  numOfAuctions
        auctionsAvg[b][1] /=  numOfAuctions
        auctionsAvg[b][2] /=  numOfAuctions


        auctionsAvg[b][1] = locale.currency(auctionsAvg[b][1])
        auctionsAvg[b][2] = locale.currency(auctionsAvg[b][2])




# define bidder types and the number of bidders of each type
bidderTypes = [(1, 'Random'), (1, 'Slow'), (1, 'Quick'), (1, 'Medium')]
doAuctions(500)



bidderTypes = [(1, 'Random'), (1, 'Slow'), (1, 'Quick'), (1, 'Low')]
print("\n")
doAuctions(5)


bidderTypes = [(1, 'Random'), (1, 'Slow'), (1, 'Quick'), (1, 'High')]
print("\n")
doAuctions(5)


bidderTypes = [(1, 'Slow'), (1, 'Quick'), (1, 'High')]
print("\n")
doAuctions(5)



bidderTypes = [(1, 'Random'), (1, 'Quick'), (1, 'High')]
print("\n")
doAuctions(5)


bidderTypes = [(1, 'Random'), (1, 'Slow'), (1, 'High')]
print("\n")
doAuctions(5)



bidderTypes = [(1, 'Random'), (1, 'Slow'), (1, 'Quick')]
print("\n")
doAuctions(5)


bidderTypes = [(2, 'Random'), (2, 'Slow'), (2, 'Quick')]
print("\n")
doAuctions(5)


bidderTypes = [(1, 'Random'), (1, 'Slow'), (2, 'High')]
print("\n")
doAuctions(5)