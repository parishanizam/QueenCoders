import random
from typing import List, Dict

import aStar

"""
This file can be a nice home for your move logic, and to write helper functions.

"""
def boardToMap(data: dict):
  map = {}

  for x in range(13):
    for y in range(13):
      map[(x, y)] = "."

  for x in range(13):
    map[(x, 0)]= "#"
    map[(x, 12)] = "#"
    map[(0, x)] = "#"
    map[(12, x)] = "#"

  for snakes in data["board"]["snakes"]:
    for body in snakes["body"]:
      map[(body["x"] + 1, body["y"] + 1)] = "#"

  map = add_snake_tail(data, map)
  map = remove_snake_head_next_possible_locations(data, map)

  return map

def add_snake_tail(data: dict, map):
  for snake in data['board']['snakes']:
    # Add last unit in each snake as possible move because it is likely empty after Move.
    tail = snake['body'][-1]
    map[(tail["x"] + 1, tail["y"] + 1)] = "."
  return map

def remove_snake_head_next_possible_locations(data: dict, map):
  for snake in data['board']['snakes']:
    if (snake['id'] != data['you']['id']):
      head = snake['head']
      head["x"] = head["x"] + 1
      head["y"] = head["y"] + 1
      print(f"SNAKE: {snake['name']} HEAD: {head}")
      map[(head["x"], head["y"] + 1)] = "#"
      map[(head["x"], head["y"] - 1)] = "#"
      map[(head["x"] + 1, head["y"])] = "#"
      map[(head["x"] - 1, head["y"])] = "#"
  return map

def findClosestFood(my_head: Dict[str, int], data: dict) -> str:
    closestPathSoFar = []
    dist = 500
    modifiedMap = boardToMap(data)
    modifiedMap[(my_head["x"] + 1, my_head["y"] + 1)] = "@"
    

    for food in data["board"]["food"]:
      mapCopy = modifiedMap
      mapCopy[(food["x"] + 1, food["y"] + 1)] = "$"
      path = aStar.astar_search(mapCopy, (my_head["x"] + 1, my_head["y"] + 1), (food["x"] + 1, food["y"] + 1))

      if path != None and len(path) < dist:
        closestPathSoFar = path
        dist = len(path)

    if dist == 500:
      return None

    print("path")
    print(closestPathSoFar)
    firstMove = {"x": closestPathSoFar[0][0] - 1, "y": closestPathSoFar[0][1] - 1}
    print("firstMove")
    print(firstMove)
    return coordToMove(my_head, firstMove)

def coordToMove(my_head: Dict[str, int], destination: Dict[str, int]) -> str:

  print("head coord")
  print(my_head)
  print("dest coord")
  print(destination)

  xDiff = my_head["x"] - destination["x"]
  yDiff = my_head["y"] - destination["y"]

  if xDiff == 0:
    if yDiff == 1:
      print("d")
      return "down"
    elif yDiff == -1:
      print("u")
      return "up"
    else:
      print("Tried to call coordToMove with not adjacent block")
  
  if yDiff == 0:
    if xDiff == 1:
      print("l")
      return "left"
    elif xDiff == -1:
      print("r")
      return "right"
  

  print("Tried to call coordToMove with not adjacent block")
  


  '''if destination["x"] < my_head["x"]:
    return "left"  # my destination is left of my head

   elif destination["x"] > my_head["x"]:
      return "right"  # my destination is right of my head
   elif destination["y"] < my_head["y"]:
      return "down"  # my destination is below my head
   elif destination["y"] > my_head["y"]:
      return "up"  # my destination is above my head
  '''

def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def avoid_walls(my_head: Dict[str, int], possible_moves: List[str])-> List[str]:
    if my_head["x"] == 0:
        possible_moves.remove("left")
    elif my_head["x"] == 10:
        possible_moves.remove("right")
    if my_head["y"] == 0:
        possible_moves.remove("down")
    elif my_head["y"] == 10:
        possible_moves.remove("up")

    return possible_moves

def checkMove(possible_moves, move):
  for pmove in possible_moves:
    if pmove == move:
      return True

  print("move not possible")
  print(pmove)
  return False

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    possible_moves = avoid_walls(my_head, possible_moves)

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    board_height = 11
    board_width = 11

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    closestFoodMove = findClosestFood(my_head, data)

    if closestFoodMove == None:
      return move

    if (checkMove(possible_moves, closestFoodMove)):
      return closestFoodMove


    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
