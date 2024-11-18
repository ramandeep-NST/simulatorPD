# # player1.py
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
#                 count += (m == "Cooperate")

#     if move == "Cooperate":
#         print("Cooperate")
#     else:
#         print("Defect")
# player1.py
# import sys
# import time
 
# O(n)
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
    count = 0
    if len(moves) > 0:
        for mm in moves:
                for n in moves:  
                    count += (mm == "Cooperate")
    

    if count >= len(moves)//2 and len(moves) == "Cooperate":
        return "Cooperate"
    else:
        return "Defect"
    
    return ""