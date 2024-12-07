import ast
import random
import os
import timeit
from typing import NamedTuple
from collections.abc import Iterator
import keyword
from concurrent.futures import ThreadPoolExecutor, as_completed
from pymongo import MongoClient,errors
import certifi

nameToScore = {}
emailToName = {}
# Points system for Prisoner's Dilemma
POINTS = {
    ("cooperate", "cooperate"): (3, 3),
    ("cooperate", "defect"): (0, 5),
    ("defect", "cooperate"): (5, 0),
    ("defect", "defect"): (1, 1)
}

# strategyValidator class , custom validator (optional)
# basic error check is handled by parse module
class StrategyValidator(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if len(node.args.args) == 0:
            self.errors.append(f"Function '{node.name}' should have at least one parameter.")
        else:
            moves_found = False
            for arg in node.args.args:
                if arg.arg == 'moves':
                    moves_found = True
            if not moves_found:
                self.errors.append(f"Function '{node.name}' must have a parameter called 'moves'.")
        
        return_statements = [n for n in node.body if isinstance(n, ast.Return)]
        if len(return_statements) == 0:
            self.errors.append(f"Function '{node.name} should have at least one return statement.")
        for return_stmt in return_statements:
            if not isinstance(return_stmt.value, ast.Constant):
                self.errors.append(f"Function '{node.name}' return value must be a string.")
        
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and keyword.iskeyword(target.id):
                self.errors.append(f"Cannot use Python keyword '{target.id}' as a variable name.")
        
        self.generic_visit(node)

    def report(self):
        return self.errors

# Main function to validate the strategy code
def isSemanticallyCorrect(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        return False
    
    validator = StrategyValidator()
    validator.visit(tree)
    
    errors = validator.report()
    if errors:
        for error in errors:
            print(f"Error: {error}")
        return False
    return True
 
# def detect_O_NN_time_complexity(tree):
   
#     def detect_nested_loops():
#         # Check for nested loops: for and while loops
#         for outer_loop in ast.walk(tree):
#             # If outer loop is a `for` loop
#             if isinstance(outer_loop, ast.For) and isinstance(outer_loop.target, ast.Name):
#                 for inner_loop in ast.walk(tree):
#                     if isinstance(inner_loop, ast.For) and inner_loop != outer_loop:
#                         if isinstance(inner_loop.target, ast.Name):
#                             return True
#                     elif isinstance(inner_loop, ast.While) and inner_loop != outer_loop:
#                         if isinstance(inner_loop.test, ast.Name):
#                             return True

#             # If outer loop is a `while` loop
#             elif isinstance(outer_loop, ast.While):
#                 # Check the body of the `while` loop recursively
#                 if contains_nested_while_or_for(outer_loop.body):
#                     return True
            
#         return False

#     def contains_nested_while_or_for(body):
#         """
#         This function recursively checks if there are any nested loops (both `for` and `while`)
#         within the body of the provided loop.
#         """
#         for stmt in body:
#             # If the statement is a `while` loop, check its body for nested loops
#             if isinstance(stmt, ast.While):
#                 # Recursively check if there are nested loops inside the body of the while loop
#                 if contains_nested_while_or_for(stmt.body):
#                     return True
#             elif isinstance(stmt, ast.For):
#                 # If it's a `for` loop, check if it is a nested loop
#                 if isinstance(stmt.target, ast.Name):
#                     return True

#         return False

#     # Call the function that will scan for nested loops
#     return detect_nested_loops()
# def detect_O_NN_time_complexity(tree):
   
#     def detect_nested_loops():
#         for outer_loop in ast.walk(tree):
#             if isinstance(outer_loop, ast.For) and isinstance(outer_loop.target, ast.Name):
#                 for inner_loop in ast.walk(tree):
#                     if isinstance(inner_loop, ast.For) and inner_loop != outer_loop:
#                         if isinstance(inner_loop.target, ast.Name):
#                             return True
#                     elif isinstance(inner_loop,ast.While) and inner_loop != outer_loop:
#                         if isinstance(inner_loop.test, ast.Name):
#                             return True

#             elif isinstance(outer_loop, ast.While):
#                 for inner_loop in outer_loop.body:
#                     if isinstance(inner_loop, ast.While):
#                         if isinstance(inner_loop.test, ast.Name):   
#                             return True
#                     elif isinstance(inner_loop,ast.For):
#                         if isinstance(inner_loop.target,ast.Name):
#                             return True
 
                    
            
#         return False
 

#     if detect_nested_loops():
#         print("Warning: Nested loops detected, potential O(N²) time complexity.")
#         return True  

#     return False

# def detect_infinite_loops(tree):
       
#         def is_infinite_loop(node):
#          if isinstance(node, ast.While):
#             if isinstance(node.test, ast.Constant) and node.test.value is True:
#                 return True

#          if isinstance(node, ast.For):
#             if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name):
#                 func_name = node.iter.func.id
#                 if func_name == 'range':
#                     args = node.iter.args
#                     if len(args) == 2 and isinstance(args[0], ast.Constant) and isinstance(args[1], ast.Constant):
#                         if args[0].value >= args[1].value:
#                             return True
#             return False

#         def detect_loops():
#          for node in ast.walk(tree):
#             if is_infinite_loop(node):
#                 return True
#          return False

#         if detect_loops():
#          print("Warning: Infinite loop detected!")
#          return True 
        

#         return False
       


def connect_to_mongo(mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri,tlsCAFile=certifi.where())
    db = client[db_name]
    collection = db[collection_name]
    return collection


def update_score_in_mongodb(mongo_uri, db_name, collection_name, strategy_name, score):
    collection = connect_to_mongo(mongo_uri, db_name, collection_name)
 
    print(f"Attempting to update strategy '{strategy_name}' with score {score}")
    try:
     result = collection.update_one(
            {"email": strategy_name},   
            {"$set": {"score": score}}   
        )
        
       
     if result.matched_count == 0:
        print(f"No strategy found with id '{strategy_name}' to update.")
        error = f"No strategy found with id '{strategy_name}' to update."
        result = collection.update_one(
            {"email":strategy_name},
            {"$set":{"error":error}}
        )
     else:
        print(f"Matched {result.matched_count} document(s) for '{strategy_name}'.")

        
     if result.modified_count > 0:
        print(f"Successfully updated score for '{strategy_name}' in Database.")
 
     else:
        print(f"No changes were made to the score for '{strategy_name}'.")

    
    except errors.PyMongoError as e:
        print(f"Error occurred while updating Database: {e}")
        result = collection.update_one(
            {"email":strategy_name},
            {"$set":{"error":e}}
        )
        raise

    

def load_strategies_from_mongodb(mongo_uri, db_name, collection_name):
    
    collection = connect_to_mongo(mongo_uri, db_name, collection_name)
    print(f"Found {collection.count_documents({})} strategies in Database")
    strategies = {}
 
    # Fetch the strategy documents
    for doc in collection.find():  
        strategy_name = doc.get('email')   
        code_content = doc.get('code')  
        name = doc.get('name')
        nameToScore[strategy_name] = name
        
        
        if not code_content:
            print(f"Skipping strategy {strategy_name} as the code is empty or None.")
            error = f"Skipping strategy {strategy_name} as the code is empty or None."
            result = collection.update_one(
                {"email":strategy_name},
                {"$set":{"error":error}}
            )
            continue
        
        
        try:
            tree = ast.parse(code_content)  
        except SyntaxError as e:
            print(f"Skipping strategy {strategy_name} due to syntax error in code: {e}")
            error = f"Skipping strategy {strategy_name} due to syntax error in code: {e}"
            result = collection.update_one(
                {"email":strategy_name},
                {"$set":{"error":error}}
            )
            continue

        # if detect_O_NN_time_complexity(tree):
        #     print(f"Stragety Submitted by {name} is of O(N*N) complexity and not allowed")
        #     error = f"Stragety Submitted by {name} is of O(N*N) complexity and not allowed"
        #     result = collection.update_one(
        #         {"email":strategy_name},
        #         {"$set":{"error":error}}
        #     )
        #     continue

        # if detect_infinite_loops(tree):
        #     print(f"Stragety Submitted by {name} contains infinite loop and not allowed")
        #     error = f"Stragety Submitted by {name} contains infinite loop and not allowed"
        #     result = collection.update_one(
        #         {"email":strategy_name},
        #         {"$set":{"error":error}}
        #     )
        #     continue
       
        
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                code = compile(ast.Module(body=[node], type_ignores=[]), filename="<ast>", mode="exec")
                local_vars = {}
                exec(code, {"random": random}, local_vars)
                strategies[strategy_name] = local_vars[node.name]
        # else:
        #     print(f"Skipping strategy {strategy_name} due to errors.")
    
    return strategies

 
def initialize_generators(strategies):
    def wrapper(strategy_fn):
        try:
            strategy_fn([])   
            return strategy_fn
        except TypeError:
            return lambda moves: strategy_fn()

    strategy_generators = {}
    for name, strategy_fn in strategies.items():
        strategy_generators[name] = wrapper(strategy_fn)
    return strategy_generators

def validate_move(move):
    if move is None:
        move = "cooperate" 

    move = move.lower()    
    if move not in {"cooperate", "defect"}:
        print(f"Invalid move '{move}' encountered. Defaulting to 'cooperate'.")
        return "cooperate"
    return move



def play_rounds(strategies,strategy_fn1, strategy_fn2, rounds=10):
    score1, score2 = 0, 0
    moves1, moves2 = [], []
     

    for _ in range(rounds):
         
        move1 = validate_move(strategy_fn1(moves2))  # Pass moves2 (opponent's moves) to strategy_fn1
        move2 = validate_move(strategy_fn2(moves1))  # Pass moves1 to strategy_fn2
        moves1.append(move1)
        moves2.append(move2)
        print(move1, move2)
        
        points1, points2 = POINTS[(move1, move2)]
        score1 += points1
        score2 += points2

    return score1, score2

def run_tournament(strategies,strategy_generators, mongo_uri, db_name, collection_name, rounds=10):

    leaderboard = {name: 0 for name in strategy_generators.keys()}
    visited = {name1 + name2: 0 for name1 in strategy_generators.keys() for name2 in strategy_generators.keys() if name1 != name2}
    
    sum = 0
    start = timeit.default_timer()
    for name1, strategy_fn1 in strategy_generators.items():
        for name2, strategy_fn2 in strategy_generators.items():
            if name1 != name2 and visited[(name1+name2)] == 0 and visited[(name2+name1)] == 0:
                with ThreadPoolExecutor(max_workers=30) as executor:
                    future = executor.submit(play_rounds, strategies,strategy_fn1, strategy_fn2, rounds)  
                    score1, score2 = future.result() 
                    leaderboard[name1] += score1
                    leaderboard[name2] += score2
                
                visited[(name1+name2)] = visited[(name2+name1)] = True
    
    end = timeit.default_timer()
    sum += (end - start)
    print(sum)
    
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)

    for strategy_name, score in sorted_leaderboard:
        update_score_in_mongodb(mongo_uri, db_name, collection_name, strategy_name, score)
    
    return sorted_leaderboard

def simulate(mongo_uri, db_name, collection_name, rounds=10):
    strategies = load_strategies_from_mongodb(mongo_uri, db_name, collection_name)
    strategy_generators = initialize_generators(strategies)
    leaderboard = run_tournament(strategies,strategy_generators,mongo_uri, db_name, collection_name,rounds)
    print("Tournament Results:")
    for email, score in leaderboard:
        print(f"{nameToScore[email]}: {email} : {score}")
 

simulate(mongo_uri, db_name, collection_name, rounds=50)

