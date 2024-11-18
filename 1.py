# # player1.py
# import sys
# import time
 
# # O(n)
 
# print("Cooperate")
# while True:

#     move = input()

#     if move == "stop":
#         break
 
#     if move == "Cooperate":
#         print("Cooperate")
#     else:
#         print("Defect")
# player1.py
# import sys
# import time
 
# # O(n)
# moves = []
# print("Cooperate")
# while True:

#     move = input()

#     if move == "stop":
#         break
    
#     moves.append(move)
#     flag = False
#     count = 0
#     if len(moves) > 0:
#         for m in moves:
#                 for n in moves:  
#                     count += (m == "Cooperate")

#     if move == "Cooperate":
#         print("Cooperate")
#     else:
#         print("Defect")

def make_moves(moves):
    if moves == []:  # First move is "Cooperate" when no opponent moves yet
        return "Cooperate"
    else:
        return "Defect"  # Return "Defect" for all subsequent moves
    

    return ""
    # Use yeild
    # While loop lagayae bacha 
    # 
    