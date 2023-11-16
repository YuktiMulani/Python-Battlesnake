# BASCILOUS PYTHON

import random
import typing
import heapq

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "yukine",  # TODO: Your Battlesnake Username
        "color": "#FFFFFF",  # TODO: Choose color
        "head": "evil",  # TODO: Choose head
        "tail": "round-bum",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def calculate_distance(start, end):
  return abs(start['x'] - end['x']) + abs(start['y'] - end['y'])

def a_star_search(start, goal, is_move_safe, game_state):
    heap = [(0, tuple(start.items()))]
    visited = set()
  
    while heap:
        cost, current = heapq.heappop(heap)
  
        if dict(current) == goal:
            return cost
  
        if current in visited:
            continue
  
        visited.add(current)
        currdic=dict((x,y)for x,y in current)
        for next_move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_dict = currdic
            neighbor = {'x': neighbor_dict['x'] + next_move[0], 'y': neighbor_dict['y'] + next_move[1]}
            neighbor_cost = cost + 1



  
            if (
                0 <= neighbor['x'] < game_state['board']['width']
                and 0 <= neighbor['y'] < game_state['board']['height']
                and is_move_safe.get(move := get_move_direction(dict(current), neighbor))
          ):
              heapq.heappush(heap, (neighbor_cost + calculate_distance(neighbor, goal), tuple(neighbor.items())))

    return float('inf')


def get_move_direction(head, neighbor):
  if head['x'] == neighbor['x']:
      return 'up' if neighbor['y'] > head['y'] else 'down'
  else:
      return 'right' if neighbor['x'] > head['x'] else 'left'
# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    print(game_state)
    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    #Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head["x"] == 0:
      is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
      is_move_safe["right"] = False
    if my_head["y"] == 0:
      is_move_safe["down"] = False
    if my_head["y"] == board_height - 1:
      is_move_safe["up"] = False
      
    
  
    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    for body_part in my_body[1:]:
      if body_part['x']==my_head['x']+1and body_part['y']==my_head['y']:
        is_move_safe["right"]=False
      if body_part['x']==my_head['x']-1and body_part['y']==my_head['y']:
        is_move_safe["left"]=False
      if body_part['x']==my_head['x'] and body_part['y']==my_head['y']+1:
        is_move_safe["up"]=False
      if body_part['x']==my_head['x'] and body_part['y']==my_head['y']-1:
        is_move_safe["down"]=False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for snake in opponents:
      for body_part in snake['body']:
        if body_part['x']==my_head['x']+1and body_part['y']==my_head['y']:
          is_move_safe["right"]=False
        if body_part['x']==my_head['x']-1and body_part['y']==my_head['y']:
          is_move_safe["left"]=False
        if body_part['x']==my_head['x'] and body_part['y']==my_head['y']+1:
          is_move_safe["up"]=False
        if body_part['x']==my_head['x'] and body_part['y']==my_head['y']-1:
          is_move_safe["down"]=False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    # Prioritize food if there's any on the board
    if game_state['board']['food']:
        # Calculate the distance to each food item using A* pathfinding
        food_distances = {}
        for food in game_state['board']['food']:
            food_id = food.get('id', None)
            if food_id is not None:
              distance = a_star_search(my_head, food, is_move_safe, game_state)
              food_distances[food['id']] = distance

        # Sort food items by distance in ascending order
        sorted_food = sorted(food_distances.items(), key=lambda x: x[1])

        # Iterate through the sorted food items and choose the move that brings you closer to the nearest food
        for food_id, distance in sorted_food:
            food_coordinates = next(({'x': f['x'], 'y': f['y']} for f in game_state['board']['food'] if f['id'] == food_id), None)

            if food_coordinates:
                dx = food_coordinates['x'] - my_head['x']
                dy = food_coordinates['y'] - my_head['y']

                # Choose the move that minimizes the distance between your head and the food
                if dx > 0 and is_move_safe["right"]:
                    return {"move": "right"}

                if dx < 0 and is_move_safe["left"]:
                    return {"move": "left"}

                if dy > 0 and is_move_safe["up"]:
                    return {"move": "up"}

                if dy < 0 and is_move_safe["down"]:
                    return {"move": "down"}  
    # Check for smaller snakes nearby and try to move towards them
    for snake in game_state['board']['snakes']:
      if len(snake['body']) < len(game_state['you']['body']):
          # The opponent snake is smaller than your snake
          dx = snake['head']['x'] - my_head['x']
          dy = snake['head']['y'] - my_head['y']

          # Calculate the expected size difference by the time your snake reaches the opponent's head
          size_difference = len(snake['body']) - len(game_state['you']['body'])

          # Move towards the smaller snake's head only if it is not expected to grow larger
          if size_difference <= 0:
              if dx > 0 and is_move_safe["right"]:
                  return {"move": "right"}

              elif dx < 0 and is_move_safe["left"]:
                  return {"move": "left"}

              elif dy > 0 and is_move_safe["up"]:
                  return {"move": "up"}

              elif dy < 0 and is_move_safe["down"]:
                  return {"move": "down"}
    # if no safe moves are left then take a default move
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)
    print(safe_moves)
  
    # print(f"MOVE {game_state['turn']}: {next_move} towards {target_

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })


# # a snake that just loops clockwise[LOOPY PYTHON]
# import random
# import typing

# def info() -> typing.Dict:
#     print("INFO")
#     return {
#         "apiversion": "1",
#         "author": "",
#         "color": "#000000",
#         "head": "evil",
#         "tail": "coffee",
#     }


# def start(game_state: typing.Dict):
#     print("GAME START")


# def end(game_state: typing.Dict):
#     print("GAME OVER\n")

# def move(game_state: typing.Dict) -> typing.Dict:

#     moves = ["up", "right", "down", "left"] # Direction order for the loop
#     # Returns the move based on the game_state['turn'] % 4
#     # As it is a cyclic sequence of 4 directions, it does not matter when the game starts, 
#     # we can ensure it always makes the loop "up" -> "right" -> "down" -> "left"
#     next_move = moves[game_state['turn'] % 4]
#     return {"move": next_move}

# if __name__ == "__main__":
#     from server import run_server

#     run_server({
#         "info": info, 
#         "start": start, 
#          "move": move, 
#         "end": end
#     })
