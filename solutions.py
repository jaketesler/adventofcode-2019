from helpers import *
import math

############
# puzzle 1 #
############
## 1 ##
def puzzle1():
  with open('d1_input.txt', 'r') as f: values = [int(v.strip()) for v in f.readlines()]
  calc_fuel = lambda v: math.floor(v/3)-2
  fuel_total = sum([calc_fuel(val) for val in values])
  print(f"Puzzle 1: {fuel_total=}")

## 1.5 ##
def puzzle15():
  with open('d1_input.txt', 'r') as f: values = [int(v.strip()) for v in f.readlines()]
  calc_fuel = lambda v: math.floor(v/3)-2
  fuel_total = 0
  for val in values:
    while (val := calc_fuel(val)) > 0: fuel_total += val
  print(f"Puzzle 1.5: {fuel_total=}")

############
# puzzle 2 #
############
## 2 ##
def puzzle2():
  with open('d2_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
  values[1] = 12; values[2] = 2 # manual modifications
  for ptr in range(0, len(values), 4):
    if   values[ptr] == 99: break
    elif values[ptr] == 1: values[values[ptr+3]] = values[values[ptr+1]] + values[values[ptr+2]]
    elif values[ptr] == 2: values[values[ptr+3]] = values[values[ptr+1]] * values[values[ptr+2]]
  print(f"Puzzle 2: {values[0]=}") # ','.join([str(v) for v in values])

## 2.5 ##
def puzzle25():
  for noun in range(0, 100):
    for verb in range(0, 100):
      with open('d2_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
      values[1] = noun; values[2] = verb # modifications
      for ptr in range(0, len(values), 4):
        if   values[ptr] == 99: break
        elif values[ptr] == 1: values[values[ptr+3]] = values[values[ptr+1]] + values[values[ptr+2]]
        elif values[ptr] == 2: values[values[ptr+3]] = values[values[ptr+1]] * values[values[ptr+2]]
      if values[0] == 19690720:
        print(f"Puzzle 2.5: (100 * noun + verb)= {100 * noun + verb}")
        return

############
# puzzle 3 #
############
## 3 ##
def puzzle3():
  with open('d3_input.txt', 'r') as f: w1, w2 = map(lambda x: x.strip().split(','), f.readlines())
  w1_locs = []; w2_locs = []
  for (w, locs) in ((w1, w1_locs), (w2, w2_locs)):
    w_pos = [0,0]
    for path in w:
      start_pos = w_pos[:]
      if   path[0] == 'U': w_pos[1] += int(path[1:])
      elif path[0] == 'D': w_pos[1] -= int(path[1:])
      elif path[0] == 'L': w_pos[0] -= int(path[1:])
      elif path[0] == 'R': w_pos[0] += int(path[1:])
      locs.append([tuple(start_pos), tuple(w_pos)])
  w_overlaps = [tuple(pt) for line1 in w1_locs for line2 in w2_locs if (pt := (line_intersection(line1, line2) or [0,0])) != [0,0]]
  w_manhattan = sorted([manhattan((0,0), pt) for pt in set(w_overlaps)])
  print(f"Puzzle 3: Shortest manhattan is {w_manhattan[0]}")

## 3.5 ##
def puzzle35():
  with open('d3_input.txt', 'r') as f: w1, w2 = map(lambda x: x.strip().split(','), f.readlines())
  w1_locs = []; w2_locs = []
  for (w, locs) in ((w1, w1_locs), (w2, w2_locs)):
    w_pos = [0,0]
    step_count = 0
    for path in w:
      start_pos = w_pos[:]
      val = int(path[1:])
      if   path[0] == 'U': w_pos[1] += val
      elif path[0] == 'D': w_pos[1] -= val
      elif path[0] == 'L': w_pos[0] -= val
      elif path[0] == 'R': w_pos[0] += val
      locs.append({'start': tuple(start_pos), 'end': tuple(w_pos), 'steps': step_count, 'dir': path[0]})
      step_count += val
  w_overlaps = []
  for line1 in w1_locs:
    for line2 in w2_locs:
      pt = line_intersection((line1['start'], line1['end']), (line2['start'], line2['end']))
      if (pt or [0,0]) != [0,0]:
        if   line1['dir'] in ('U','D'): l1_dtoi = abs(line1['start'][1] - pt[1])
        elif line1['dir'] in ('L','R'): l1_dtoi = abs(line1['start'][0] - pt[0])
        if   line2['dir'] in ('U','D'): l2_dtoi = abs(line2['start'][1] - pt[1])
        elif line2['dir'] in ('L','R'): l2_dtoi = abs(line2['start'][0] - pt[0])
        total_steps = line1['steps'] + line2['steps'] + l1_dtoi + l2_dtoi
        w_overlaps.append(total_steps)
  w_overlaps = sorted(list(set(w_overlaps)))
  print(f"Puzzle 3.5: Fewest steps is {w_overlaps[0]}")

############
# puzzle 4 #
############
## 4 ##
def puzzle4():
  d4_input = range(235741, 706948+1)
  def is_valid_4(val):
    val = [int(d) for d in str(val)]
    for idx in range(0, 5): # digits LR check
      if val[idx+1] < val[idx]: return False
    for idx in range(0, 5): # adjacent matching digits check
      if val[idx] == val[idx+1]: return True
    return False
  count = sum([1 for val in d4_input if is_valid_4(val)])
  print(f"Puzzle 4: Total possible passwords: {count}")

## 4.5 ##
def puzzle45():
  d4_input = range(235741, 706948+1)
  def is_valid_45(val):
    val = [int(d) for d in str(val)]
    for idx in range(0, 5): # digits LR check
      if val[idx+1] < val[idx]: return False
    if (val[0] == val[1] and
        val[1] != val[2]): return True # first pair
    for idx in range(1, 4): # middle pairs
      if (val[idx-1] != val[idx+0] and
          val[idx+0] == val[idx+1] and
          val[idx+1] != val[idx+2]): return True
    if (val[3] != val[4] and
        val[4] == val[5]): return True # last pair
    return False
  count = sum([1 for val in d4_input if is_valid_45(val)])
  print(f"Puzzle 4.5: Total possible passwords: {count}")

############
# puzzle 5 #
############
## 5 ##
def puzzle5():
  with open('d5_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
  ptr = 0
  output = []

  while ptr < len(values):
    opcode = int(str(values[ptr])[-2:]) # two rightmost digits
    modes = [int(c) for c in str(values[ptr])[:-2]][::-1] # all leftmost digits (right-to-left) # rightmost is last param
    get_param = lambda idx: values[values[ptr+idx]] if safe_list_get(modes, idx-1, 0) == 0 else values[ptr+idx]
    def update_value(idx, value):
      if safe_list_get(modes, idx-1, 0) == 0: values[values[ptr+idx]] = value # send to pointer
      else: values[ptr+idx] = value

    if   opcode == 99: break
    elif opcode == 1: update_value(3, get_param(1) + get_param(2)); ptr += 4
    elif opcode == 2: update_value(3, get_param(1) * get_param(2)); ptr += 4
    elif opcode == 3: update_value(1, int(input("Input (P5): ")));  ptr += 2
    elif opcode == 4: output.append(get_param(1)); ptr += 2
  print("Puzzle 5: {}".format(f'All tests passed! Output: {output[-1]}' if not any(output[:-1]) else f'Tests failed: {output=}'))

## 5.5 ##
def puzzle55():
  with open('d5_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
  ptr = 0
  output = []

  while ptr < len(values):
    opcode = int(str(values[ptr])[-2:]) # two rightmost digits
    modes = [int(c) for c in str(values[ptr])[:-2]][::-1] # all leftmost digits (right-to-left) # rightmost is last param
    get_param = lambda idx: values[values[ptr+idx]] if safe_list_get(modes, idx-1, 0) == 0 else values[ptr+idx]
    def update_value(idx, value):
      if safe_list_get(modes, idx-1, 0) == 0: values[values[ptr+idx]] = value # send to pointer
      else: values[ptr+idx] = value

    if   opcode == 99: break
    elif opcode == 1: update_value(3, get_param(1) + get_param(2)); ptr += 4
    elif opcode == 2: update_value(3, get_param(1) * get_param(2)); ptr += 4
    elif opcode == 3: update_value(1, int(input("Input (P5.5): "))); ptr += 2
    elif opcode == 4: output.append(get_param(1)); ptr += 2
    elif opcode == 5: ptr = get_param(2) if get_param(1) != 0 else ptr+3
    elif opcode == 6: ptr = get_param(2) if get_param(1) == 0 else ptr+3
    elif opcode == 7: values[values[ptr+3]] = int(get_param(1) <  get_param(2)); ptr += 4
    elif opcode == 8: values[values[ptr+3]] = int(get_param(1) == get_param(2)); ptr += 4
  print("Puzzle 5.5: {}".format(f'All tests passed! Output: {output[-1]}' if not any(output[:-1]) else f'Tests failed: {output=}'))

##########################
if __name__ == '__main__':
  # puzzle1()
  # puzzle15()
  # puzzle2()
  # puzzle25()
  # puzzle3()
  # puzzle35()
  # puzzle4()
  # puzzle45()
  puzzle5()
  puzzle55()
