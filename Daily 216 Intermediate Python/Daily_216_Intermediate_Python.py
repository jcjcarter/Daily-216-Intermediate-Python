from random import shuffle
from itertools import product, combinations, combinations_with_replacement

ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

r = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
s = [2, 3, 5, 7]

deck = [card for card in product(r, s)]
players = {}
community = []
hand_scores_flush = {}
hand_scores = {}
score = 1

def add_score(a,i,s,d,htype):
    if a:
        d[i] = (s,htype)
        return 1
    return 0

# Straight flush
# Straight flush
for i in reversed(range(10)):
    score += add_score(True, r[i+3]*r[i+2]*r[i+1]*r[i]*r[i-1], score, hand_scores_flush, 'Straight flush')
# Four of a kind
for i in product(reversed(r), repeat=2):
    score += add_score(i[0] != i[1], (i[0]**4)*i[1], score, hand_scores, 'Four of a kind')
# Full house
for i in product(reversed(r), repeat=2):
    score += add_score(i[0] != i[1], (i[0]**3)*i[1]**2, score, hand_scores, 'Full house')
# Flush
for i in combinations(reversed(r), 5):
    j = i[0]*i[1]*i[2]*i[3]*i[4]
    score += add_score(hand_scores_flush.get(j) == None, j, score, hand_scores_flush, 'Flush')
# Straight
for i in reversed(range(10)):
    score += add_score(True, r[i+3]*r[i+2]*r[i+1]*r[i]*r[i-1], score, hand_scores, 'Straight')
# Three of a kind
for i in product(reversed(r), combinations_with_replacement(reversed(r), 2)):
    score += add_score(i[0] != i[1][0] and i[0] != i[1][1], i[0]**3*i[1][0]*i[1][1], score, hand_scores, 'Three of a kind')
# Two pair
for i in product(combinations_with_replacement(reversed(r), 2), reversed(r)):
    score += add_score(i[0][0] != i[0][1] and i[1] != i[0][0] and i[1] != i[0][1], i[0][0]**2*i[0][1]**2*i[1], score, hand_scores, 'Two pair')
# One pair
for i in product(reversed(r), combinations(reversed(r), 3)):
    score += add_score(i[1][0] != i[0] and i[1][1] != i[0] and i[1][2] != i[0], i[0]**2*i[1][0]*i[1][1]*i[1][2], score,hand_scores, 'One pair')
# High card
for i in combinations(reversed(r), 5):
    score += add_score(hand_scores.get(i[0]*i[1]*i[2]*i[3]*i[4]) == None, i[0]*i[1]*i[2]*i[3]*i[4], score, hand_scores, 'High card')


def handscore(hand):
    suit_v = hand[0][1]*hand[1][1]*hand[2][1]*hand[3][1]*hand[4][1]
    if suit_v == 2**5 or suit_v == 3**5 or suit_v == 5**5 or suit_v == 7**5:
        return hand_scores_flush[hand[0][0]*hand[1][0]*hand[2][0]*hand[3][0]*hand[4][0]]
    return hand_scores[hand[0][0]*hand[1][0]*hand[2][0]*hand[3][0]*hand[4][0]]

scard = lambda c: '{} of {}'.format(ranks[r.index(c[0])], suits[s.index(c[1])])

def playerscore(card1, card2, c):
    hscore = [10000, None]
    for i in combinations(c, 3):
        hs = handscore([card1, card2, i[0], i[1], i[2]])
        if hs[0] < hscore[0]: hscore = hs
    if len(c) > 3:
        for j in combinations(c, 4):
            hs = handscore([card1, j[0], j[1], j[2], j[3]])
            if hs[0] < hscore[0]: hscore = hs
        for j in combinations(c, 4):
            hs = handscore([card2, j[0], j[1], j[2], j[3]])
            if hs[0] < hscore[0]: hscore = hs
    return hscore

numPlayers = int(input('How many players (2-8) ? '))
shuffle(deck)

for player in range(numPlayers): # Deal player first card
    players[player] = [deck.pop()]
for player in range(numPlayers): # Deal player second card
    players[player].append(deck.pop())
    name = "CPU {!s}'s".format(player)
    if player == 0: name = '\nYour'
    print("{} hand: {}, {}".format(name, scard(players[player][0]), scard(players[player][1])))

deck.pop() # burn a card
community = [deck.pop(), deck.pop(), deck.pop()]
print('\nFlop: {}, {}, {}'.format(scard(community[0]), scard(community[1]), scard(community[2])))

deck.pop() # burn a card
community.append(deck.pop())
print('Turn: {}'.format(scard(community[3])))

deck.pop() # burn a card
community.append(deck.pop())
print('River: {}'.format(scard(community[4])))

rankings = {}
bestPlayer = None
bestScore = 10000
for i in range(numPlayers):
    rankings[i] = playerscore(players[i][0], players[i][1], community)
    if rankings[i][0] < bestScore: 
        bestScore = rankings[i][0]
        bestplayer = i
if bestPlayer == 0: 
    print("Winner: You! {}.".format(rankings[bestPlayer][1]))
else:
    print("Winner: CPU {!s}. {}.".format(bestPlayer, rankings[bestPlayer][1]))