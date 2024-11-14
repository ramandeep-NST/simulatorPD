import ast
import random
import os
import timeit

# Points system for Prisoner's Dilemma
POINTS = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1)
}

# checks if the code does not contain an error
def isSemanticallyCorrect(tree):
    pass 
    

def load_strategies(directory):
    strategies = {}
    #isCorrect = {}
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                code_content = file.read()
                tree = ast.parse(code_content)
                # isCorrect[filename] = isSemanticallyCorrect(tree)
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        strategy_name = f"{filename}::{node.name}"
                        code = compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec")
                        local_vars = {}
                        exec(code, {"random": random}, local_vars)
                        strategies[strategy_name] = local_vars[node.name] 
    return strategies

# Ensures each function accepts a `moves` parameter for opponent history
def initialize_generators(strategies):
    def wrapper(strategy_fn):
        try:
            strategy_fn([])  # Check if it accepts a parameter
            return strategy_fn
        except TypeError:
            # Return a lambda that wraps the function to accept a moves parameter
            return lambda moves: strategy_fn()

    strategy_generators = {}
    for name, strategy_fn in strategies.items():
        strategy_generators[name] = wrapper(strategy_fn)
    return strategy_generators

def validate_move(move):
    if move not in {"Cooperate", "Defect"}:
        print(f"Invalid move '{move}' encountered. Defaulting to 'Cooperate'.")
        return "Cooperate"
    return move

def play_rounds(strategy_fn1, strategy_fn2, rounds=10):
    score1, score2 = 0, 0
    moves1, moves2 = [], []

    for _ in range(rounds):
        # Pass opponent's history to each strategy function
        move1 = validate_move(strategy_fn1(moves2))  # Pass moves2 (opponent's moves) to strategy_fn1
        move2 = validate_move(strategy_fn2(moves1))  # Pass moves1 to strategy_fn2
        moves1.append(move1)
        moves2.append(move2)
        print(move1,move2)
        
        points1, points2 = POINTS[(move1, move2)]
        score1 += points1
        score2 += points2

    return score1, score2

def run_tournament(strategy_generators, rounds=10):
    leaderboard = {name: 0 for name in strategy_generators.keys()}
    # Assuming strategy_generators is a dictionary of strategies
    visited = {name1 + name2: 0 for name1 in strategy_generators.keys() for name2 in strategy_generators.keys() if name1 != name2}
    
    sum = 0
    start = timeit.default_timer()
    for name1, strategy_fn1 in strategy_generators.items():
        for name2, strategy_fn2 in strategy_generators.items():
            if name1 != name2 and visited[(name1+name2)] == False and visited[(name2+name1)] == False:
                score1, score2 = play_rounds(strategy_fn1, strategy_fn2, rounds)
                leaderboard[name1] += score1
                leaderboard[name2] += score2
                print(type(name1))
                print(name2)
                visited[(name1+name2)] = visited[(name2+name1)] = True
    
    end = timeit.default_timer()
    sum += (end - start)
    print(sum)
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    return sorted_leaderboard

def simulate(directory, rounds=10):
    strategies = load_strategies(directory)
    strategy_generators = initialize_generators(strategies)
    leaderboard = run_tournament(strategy_generators, rounds)
    print("Tournament Results:")
    for name, score in leaderboard:
        print(f"{name}: {score}")

# Run the simulation
simulate("/Users/ramandeepsingh/Desktop/strategies", rounds=5)


# study
