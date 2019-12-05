from helpers import *
import math

############
# puzzle 1 #
############
## 1 ##
with open('d1_input.txt', 'r') as f:
  values = [int(v.strip()) for v in f.readlines()]
calc_fuel = lambda v: math.floor(v/3)-2
fuel_total = 0
for val in values:
  fuel_total += calc_fuel(val)
print(f"Puzzle 1: {fuel_total=}")

## 1.5 ##
fuel_total = 0
for val in values:
  while (val := calc_fuel(val)) > 0:
    fuel_total += val
print(f"Puzzle 1.5: {fuel_total=}")

############
# puzzle 2 #
############
## 2 ##
with open('d2_input.txt', 'r') as f:
  values = [int(v) for v in f.readlines()[0].strip().split(',')]
values[1] = 12; values[2] = 2 # manual modifications
for ptr in range(0, len(values), 4):
  if   values[ptr] == 99: break
  elif values[ptr] == 1: values[values[ptr+3]] = values[values[ptr+1]] + values[values[ptr+2]]
  elif values[ptr] == 2: values[values[ptr+3]] = values[values[ptr+1]] * values[values[ptr+2]]
print(f"Puzzle 2: {values[0]=}") # ','.join([str(v) for v in values])

## 2.5 ##
for noun in range(0, 100):
  for verb in range(0, 100):
    with open('d2_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
    values[1] = noun; values[2] = verb # manual modifications
    for ptr in range(0, len(values), 4):
      if   values[ptr] == 99: break
      elif values[ptr] == 1: values[values[ptr+3]] = values[values[ptr+1]] + values[values[ptr+2]]
      elif values[ptr] == 2: values[values[ptr+3]] = values[values[ptr+1]] * values[values[ptr+2]]
    if values[0] == 19690720:
      print(f"Puzzle 2.5: (100 * noun + verb)= {100 * noun + verb}")
      break

############
# puzzle 3 #
############
## 3 ##
with open('d3_input.txt', 'r') as f:
  w1, w2 = map(lambda x: x.strip().split(','), f.readlines())
w1_locs = []; w2_locs = []
for (w, locs) in ((w1, w1_locs), (w2, w2_locs)):
  w_pos = [0,0]
  for path in w:
    w_pos_ = w_pos[:]
    if   path[0] == 'U': w_pos[1] += int(path[1:])
    elif path[0] == 'D': w_pos[1] -= int(path[1:])
    elif path[0] == 'L': w_pos[0] -= int(path[1:])
    elif path[0] == 'R': w_pos[0] += int(path[1:])
    locs.append([tuple(w_pos_), tuple(w_pos)])
w_overlaps = [tuple(pt) for line1 in w1_locs for line2 in w2_locs if (pt := line_intersection(line1, line2)) is not None]
w_manhattan = sorted([manhattan((0,0), pt) for pt in set(w_overlaps[1:])])
print(f"Puzzle 3: Shortest manhattan is {w_manhattan[0]}")

## 3.5 ##
with open('d3_input.txt', 'r') as f:
  w1, w2 = map(lambda x: x.strip().split(','), f.readlines())
w1_locs = []; w2_locs = []
for (w, locs) in ((w1, w1_locs), (w2, w2_locs)):
  w_pos = [0,0]
  step_count = 0
  for path in w:
    w_pos_ = w_pos[:]
    val = int(path[1:])
    if   path[0] == 'U': w_pos[1] += val
    elif path[0] == 'D': w_pos[1] -= val
    elif path[0] == 'L': w_pos[0] -= val
    elif path[0] == 'R': w_pos[0] += val
    locs.append({'start': tuple(w_pos_), 'end': tuple(w_pos), 'steps': step_count, 'dir': path[0]})
    step_count += val
w_overlaps = []
for line1 in w1_locs:
  for line2 in w2_locs:
    pt = line_intersection((line1['start'], line1['end']), (line2['start'], line2['end']))
    if pt is not None and pt != [0,0]:
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
d3_input = range(235741, 706948+1)
def is_valid(val):
  val = [int(d) for d in str(val)]
  for idx in range(0, 5): # digits LR check
    if val[idx+1] < val[idx]: return False
  for idx in range(0, 5):
    if val[idx] == val[idx+1]: return True
  return False
count = sum([1 for val in d3_input if is_valid(val)])
print(f"Puzzle 4: Total possible passwords: {count}")

## 4.5 ##
d3_input = range(235741, 706948+1)
def is_valid(val):
  val = [int(d) for d in str(val)]
  for idx in range(0, 5): # digits LR check
    if val[idx+1] < val[idx]: return False
  if val[0] == val[1] and val[1] != val[2]: return True # first pair
  for idx in range(1, 4): # middle pairs
    if (val[idx-1] != val[idx+0] and
        val[idx+0] == val[idx+1] and
        val[idx+1] != val[idx+2]): return True
  if val[3] != val[4] and val[4] == val[5]: return True # last pair
  return False
count = sum([1 for val in d3_input if is_valid(val)])
print(f"Puzzle 4.5: Total possible passwords: {count}")
