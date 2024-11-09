import ast
import random
import os

# Points system for Prisoner's Dilemma
POINTS = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1)
}


def load_strategies(directory):
    strategies = {}
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            #print(filepath)
            with open(filepath, "r") as file:
                code_content = file.read()
                tree = ast.parse(code_content)
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):  
                        strategy_name = f"{filename}::{node.name}"
                        code = compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec")
                        local_vars = {}
                        exec(code, {"random": random}, local_vars)
                        strategies[strategy_name] = local_vars[node.name] 
    return strategies


def initialize_generators(strategies):
    strategy_generators = {}
    for name, strategy_fn in strategies.items():
        strategy_generators[name] = lambda moves=[]: strategy_fn()
    return strategy_generators


def play_rounds(strategy_gen1, strategy_gen2, rounds=10):
    score1, score2 = 0, 0
    moves1, moves2 = [], []
    # print(strategy_gen1)
    # print(strategy_gen2)

    gen1 = strategy_gen1(moves2)
    gen2 = strategy_gen2(moves1)

    # print(gen1)
    # print(gen2)

    # for _ in range(rounds):
    #     move1 = next(gen1)
    #     move2 = next(gen2)
    #     moves1.append(move1)
    #     moves2.append(move2)
    #     points1, points2 = POINTS[(move1, move2)]
    #     # print(points1)
    #     # print(points2)
    #     score1 += points1
    #     score2 += points2

    return score1, score2


def run_tournament(strategy_generators, rounds=10):
    leaderboard = {name: 0 for name in strategy_generators.keys()}

    print(strategy_generators)

    for name1, gen1 in strategy_generators.items():
        for name2, gen2 in strategy_generators.items():
            if name1 != name2:
                score1, score2 = play_rounds(gen1, gen2, rounds)
                leaderboard[name1] += score1
                leaderboard[name2] += score2

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    return sorted_leaderboard



def simulate(directory, rounds=10):
    strategies = load_strategies(directory)
    #print(strategies)
    strategy_generators = initialize_generators(strategies)
    #print(strategy_generators)
    leaderboard = run_tournament(strategy_generators, rounds)
   
 
simulate("/Users/ramandeepsingh/Desktop/strategies", rounds=10)
