from .Individual import Individual
from .Node import Node
import random


#
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#

def tournament(rng, population, n):
    '''
    Selects "n" Individuals from the population and return a
    single Individual.

    Parameters:
    population (list): A list of Individuals, sorted from best to worse.
    '''
    candidates = [rng.randint(0, len(population) - 1) for i in range(n)]
    return population[min(candidates)]


def parsimony_tournament(rng, population, n):
    candidates = [rng.randint(0, len(population) - 1) for i in range(n)]

    # initializing a winner and his index
    winner_index = candidates[0]
    winner = population[candidates[0]]

    # selecting the shortest individual
    for candidate in candidates:
        if len(str(population[candidate])) < len(str(winner)):
            winner = population[candidate]
            winner_index = candidate

    return winner, winner_index


def double_tournament(rng, population, n_DT, Sf, Sp, switch=False):
    if switch == False:
        candidates = []
        for i in range(Sf):
            candidates.append(tournament(rng, population, n_DT))
        winner = parsimony_tournament(rng, candidates, Sp)[0]

    else:
        candidates_tup = []
        for i in range(Sp):
            candidates_tup.append(parsimony_tournament(rng, population, n_DT))
        candidates_tup.sort(
            key=lambda x: x[1])  # sorting the candidates by their index that also means to sort them by their fitness
        candidates = list(zip(*candidates_tup))[0]  # taking the first element from each tuple
        winner = tournament(random, candidates, Sf)

    return winner


def getElite(population, n):
    '''
    Returns the "n" best Individuals in the population.

    Parameters:
    population (list): A list of Individuals, sorted from best to worse.
    '''
    return population[:n]


def getOffspring(rng, population, n_DT, Sf, Sp, switch):
    '''
    Genetic Operator: Selects a genetic operator and returns a list with the
    offspring Individuals. The crossover GOs return two Individuals and the
    mutation GO returns one individual. Individuals over the LIMIT_DEPTH are
    then excluded, making it possible for this method to return an empty list.

    Parameters:
    population (list): A list of Individuals, sorted from best to worse.
    '''
    isCross = rng.random() < 0.5

    desc = None

    if isCross:
        desc = STXO(rng, population, n_DT, Sf, Sp, switch)
    else:
        desc = STMUT(rng, population, n_DT, Sf, Sp, switch)

    return desc


def discardDeep(population, limit):
    ret = []
    for ind in population:
        if ind.getDepth() <= limit:
            ret.append(ind)
    return ret


def STXO(rng, population, n_DT, Sf, Sp, switch):
    '''
    Randomly selects one node from each of two individuals; swaps the node and
    sub-nodes; and returns the two new Individuals as the offspring.

    Parameters:
    population (list): A list of Individuals, sorted from best to worse.
    '''
    ind1 = double_tournament(rng, population, n_DT, Sf, Sp, switch)
    ind2 = double_tournament(rng, population, n_DT, Sf, Sp, switch)

    h1 = ind1.getHead()
    h2 = ind2.getHead()

    n1 = h1.getRandomNode(rng)
    n2 = h2.getRandomNode(rng)

    n1.swap(n2)

    ret = []
    for h in [h1, h2]:
        i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
        i.copy(h)
        ret.append(i)
    return ret


def STMUT(rng, population, n_DT, Sf, Sp, switch):
    '''
    Randomly selects one node from a single individual; swaps the node with a
    new, node generated using Grow; and returns the new Individual as the offspring.

    Parameters:
    population (list): A list of Individuals, sorted from best to worse.
    '''
    ind1 = double_tournament(rng, population, n_DT, Sf, Sp, switch)
    h1 = ind1.getHead()
    n1 = h1.getRandomNode(rng)
    n = Node()
    n.create(rng, ind1.operators, ind1.terminals, ind1.max_depth)
    n1.swap(n)

    ret = []
    i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
    i.copy(h1)
    ret.append(i)
    return ret
