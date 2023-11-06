# BASCILOUS PYTHON

# import random
# import typing


# # info is called when you create your Battlesnake on play.battlesnake.com
# # and controls your Battlesnake's appearance
# # TIP: If you open your Battlesnake URL in a browser you should see this data
# def info() -> typing.Dict:
#     print("INFO")

#     return {
#         "apiversion": "1",
#         "author": "yukine",  # TODO: Your Battlesnake Username
#         "color": "#000000",  # TODO: Choose color
#         "head": "evil",  # TODO: Choose head
#         "tail": "coffee",  # TODO: Choose tail
#     }


# # start is called when your Battlesnake begins a game
# def start(game_state: typing.Dict):
#     print("GAME START")


# # end is called when your Battlesnake finishes a game
# def end(game_state: typing.Dict):
#     print("GAME OVER\n")

# def is_in_bounds(x, y, game_state):
#   board_width = game_state['board']['width']
#   board_height = game_state['board']['height']
#   return 0 <= x < board_width and 0 <= y < board_height


# # move is called on every turn and returns your next move
# # Valid moves are "up", "down", "left", or "right"
# # See https://docs.battlesnake.com/api/example-move for available data
# def move(game_state: typing.Dict) -> typing.Dict:

#     is_move_safe = {
#       "up": True, 
#       "down": True, 
#       "left": True, 
#       "right": True
#     }

#     # We've included code to prevent your Battlesnake from moving backwards
#     my_head = game_state["you"]["body"][0]  # Coordinates of your head
#     my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

#     if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
#         is_move_safe["left"] = False

#     elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
#         is_move_safe["right"] = False

#     elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
#         is_move_safe["down"] = False

#     elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
#         is_move_safe["up"] = False

#     # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
#     board_width = game_state['board']['width']
#     board_height = game_state['board']['height']
#     if my_head["x"]==0:
#       is_move_safe["left"]=False
#     elif my_head["x"]==board_width-1:
#       is_move_safe["right"]=False
#     elif my_head["y"]==0:
#       is_move_safe["up"]=False
#     elif my_head["y"]==board_width-1:
#       is_move_safe["down"]=False
#     elif my_head["x"]==0 and my_head["y"]==0:
#       is_move_safe["left"]=False
#       is_move_safe["up"]=False
#       is_move_safe["right"]=True
#       is_move_safe["down"]=False
#     elif my_head["x"]==board_width-1 and my_head["y"]==board_width-1:
#       is_move_safe["right"]=False
#       is_move_safe["up"]=False
#       is_move_safe["left"]=True
#       is_move_safe["down"]=False
#     # elif my_head["x"]==0 and my_head["y"]==board_width-1:

#     # if not is_in_bounds(my_head["x"]-1, my_head["y"], game_state):
#     #   is_move_safe["left"] = False
#     # if not is_in_bounds(my_head["x"]+1, my_head["y"], game_state):
#     #   is_move_safe["right"] = False
#     # if not is_in_bounds(my_head["x"], my_head["y"]-1, game_state):
#     #   is_move_safe["up"] = False
#     # if not is_in_bounds(my_head["x"], my_head["y"]+1, game_state):
#     #   is_move_safe["down"] = False
  
#     # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
#     my_body = game_state['you']['body']
#     for body_part in my_body[1:]:
#       if body_part['x']==my_head['x']+1and body_part['y']==my_head['y']:
#         is_move_safe["right"]=False
#       if body_part['x']==my_head['x']-1and body_part['y']==my_head['y']:
#         is_move_safe["left"]=False
#       if body_part['x']==my_head['x'] and body_part['y']==my_head['y']+1:
#         is_move_safe["down"]=False
#       if body_part['x']==my_head['x'] and body_part['y']==my_head['y']-1:
#         is_move_safe["up"]=False

#     # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
#     opponents = game_state['board']['snakes']
#     for opponent in opponents:
#       for body_part in opponent['body']:
#         if body_part['x']==my_head['x']+1and body_part['y']==my_head['y']:
#           is_move_safe["right"]=False
#         if body_part['x']==my_head['x']-1and body_part['y']==my_head['y']:
#           is_move_safe["left"]=False
#         if body_part['x']==my_head['x'] and body_part['y']==my_head['y']+1:
#           is_move_safe["down"]=False
#         if body_part['x']==my_head['x'] and body_part['y']==my_head['y']-1:
#           is_move_safe["up"]=False

#     # Are there any safe moves left?
#     safe_moves = []
#     for move, isSafe in is_move_safe.items():
#         if isSafe:
#             safe_moves.append(move)

#     if len(safe_moves) == 0:
#         print(f"MOVE {game_state['turn']}: No safe moves detected! Moving up")
#         return {"move": "up"}

#     # Choose a random move from the safe ones
#     # next_move = random.choice(safe_moves)
#     next_move = ''
#     if len(safe_moves)>0:
#       next_move=random.choice(safe_moves)
#     else:
#       next_move="up"

  
#     # 

#     # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
#     food = game_state['board']['food']
#     sorted_food=sorted(food, key=lambda f: abs(my_head['x'] - f['x']) + abs(my_head['y'] - f['y']))
#     # best_food=None
#     # best_distance=float('inf')
  
#    #find the nearest food for the snake
#     for best_food in sorted_food:
#       if best_food['x']>my_head['x']:
#         target_direction='right'
#       elif best_food['x']<my_head['x']:
#         target_direction='left'
#       elif best_food['y']>my_head['y']:
#         target_direction='down'
#       elif best_food['y']<my_head['y']:
#         target_direction='up'
#       if target_direction in safe_moves:
#         next_move=target_direction
#         break
#       else:
#         if len(safe_moves)>0:
#           sort_funcs = {
#               "left": lambda f: abs((my_head['x']-1) - f['x']) + abs(my_head['y'] - f['y']),
#               "right": lambda f: abs((my_head['x']+1) - f['x']) + abs(my_head['y'] - f['y']),
#               "up": lambda f: abs(my_head['x'] - f['x']) + abs((my_head['y']-1) - f['y']),
#               "down": lambda f: abs(my_head['x'] - f['x']) + abs((my_head['y']+1) - f['y'])
#           }
#           sort_functions = [(i, sort_funcs[i](best_food)) for i in safe_moves]
#           sort_functions.sort(key=lambda x: x[1])
#           next_move = sort_functions[0][0]
#         else:
#           next_move="up"

        
#     # print(f"MOVE {game_state['turn']}: {next_move} towards {target_

#     print(f"MOVE {game_state['turn']}: {next_move}")
#     return {"move": next_move}


# # Start server when `python main.py` is run
# if __name__ == "__main__":
#     from server import run_server

#     run_server({
#         "info": info, 
#         "start": start, 
#          "move": move, 
#         "end": end
#     })


# a snake that just loops clockwise[LOOPY PYTHON]
import random
import typing

def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "",
        "color": "#000000",
        "head": "evil",
        "tail": "coffee",
    }


def start(game_state: typing.Dict):
    print("GAME START")


def end(game_state: typing.Dict):
    print("GAME OVER\n")

def move(game_state: typing.Dict) -> typing.Dict:

    moves = ["up", "right", "down", "left"] # Direction order for the loop
    # Returns the move based on the game_state['turn'] % 4
    # As it is a cyclic sequence of 4 directions, it does not matter when the game starts, 
    # we can ensure it always makes the loop "up" -> "right" -> "down" -> "left"
    next_move = moves[game_state['turn'] % 4]
    return {"move": next_move}

if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
