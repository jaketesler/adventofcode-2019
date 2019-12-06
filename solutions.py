from helpers import *
import math
import itertools

get = safe_list_get

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
  for noun, verb in itertools.product(range(0, 100), range(0, 100)):
    with open('d2_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
    values[1] = noun; values[2] = verb # modifications
    for ptr in range(0, len(values), 4):
      if   values[ptr] == 99: break
      elif values[ptr] == 1: values[values[ptr+3]] = values[values[ptr+1]] + values[values[ptr+2]]
      elif values[ptr] == 2: values[values[ptr+3]] = values[values[ptr+1]] * values[values[ptr+2]]
    if values[0] == 19690720: return print(f"Puzzle 2.5: (100 * noun + verb)= {100 * noun + verb}")

############
# puzzle 3 #
############
## 3 ##
def puzzle3():
  with open('d3_input.txt', 'r') as f: w1, w2 = map(lambda x: x.strip().split(','), f.readlines())
  w1_locs = []; w2_locs = []
  for w, locs in ((w1, w1_locs), (w2, w2_locs)):
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
  for w, locs in ((w1, w1_locs), (w2, w2_locs)):
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

  # LONG
  # w_overlaps = []
  # for line1, line2 in itertools.product(w1_locs, w2_locs):
  #   if (pt or [0,0]) == [0,0]: continue # skip
  #   if   line1['dir'] in ('U','D'): l1_dtoi = abs(line1['start'][1] - pt[1])
  #   elif line1['dir'] in ('L','R'): l1_dtoi = abs(line1['start'][0] - pt[0])
  #   if   line2['dir'] in ('U','D'): l2_dtoi = abs(line2['start'][1] - pt[1])
  #   elif line2['dir'] in ('L','R'): l2_dtoi = abs(line2['start'][0] - pt[0])
  #   total_steps = line1['steps'] + line2['steps'] + l1_dtoi + l2_dtoi
  #   w_overlaps.append(total_steps)

  # Comprehension
  w_overlaps = sorted(list(set([sum([abs((line['start'][1] - pt[1]) if line['dir'] in ('U','D') else (line['start'][0] - pt[0])) + line['steps'] for line in (line1, line2)]) for line1, line2 in itertools.product(w1_locs, w2_locs) if ((pt := line_intersection((line1['start'], line1['end']), (line2['start'], line2['end']))) or [0,0] != [0,0])])))

  # Comprehension (expanded)
  # w_overlaps = sorted(list(set(
  #   [
  #     sum([
  #       abs((line['start'][1] - pt[1]) if line['dir'] in ('U','D') else (line['start'][0] - pt[0])) + line['steps']
  #         for line in (line1, line2)
  #     ])
  #     for line1, line2 in itertools.product(w1_locs, w2_locs)
  #     if (pt := line_intersection((line1['start'], line1['end']), (line2['start'], line2['end']))) or [0,0] != [0,0]
  #   ]
  # )))
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
    for idx in range(0, 5):
      if (get(val, idx-1, val[idx+1]) != get(val, idx+0, get(val, idx+2, val[idx-1])) and
          get(val, idx+0, val[idx+0]) == get(val, idx+1, val[idx+0]) and
          get(val, idx+1, val[idx+0]) != get(val, idx+2, val[idx-1])): return True
    return False
  count = sum([1 for val in d4_input if is_valid_45(val)])
  print(f"Puzzle 4.5: Total possible passwords: {count}")

############
# puzzle 5 #
############
## 5 ##
def puzzle5():
  with open('d5_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
  get_param = lambda idx: values[values[ptr+idx]] if get(modes, idx-1, 0) == 0 else values[ptr+idx]
  def update_value(idx, value): v_idx = values[ptr+idx] if get(modes, idx-1, 0) == 0 else ptr+idx; values[v_idx] = value
  ptr = 0
  output = []
  while ptr < len(values):
    modes = [int(c) for c in str(values[ptr])[:-2]][::-1] # all leftmost digits (right-to-left) # rightmost is last param
    opcode = int(str(values[ptr])[-2:])                   # two rightmost digits
    if   opcode == 99: break
    elif opcode == 1: update_value(3, get_param(1) + get_param(2)); ptr += 4
    elif opcode == 2: update_value(3, get_param(1) * get_param(2)); ptr += 4
    elif opcode == 3: update_value(1, int(input("Input (P5): ")));  ptr += 2
    elif opcode == 4: output.append(get_param(1)); ptr += 2
  print("Puzzle 5: {}".format(f'All tests passed! Output: {output[-1]}' if not any(output[:-1]) else f'Tests failed: {output=}'))

## 5.5 ##
def puzzle55():
  with open('d5_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
  vpos = lambda m_idx: values[ptr+m_idx] if get(modes, m_idx-1, 0) == 0 else ptr+m_idx # given a mode index, calculate the proper position for indexing into values
  ptr = 0
  while ptr < len(values):
    modes = [int(c) for c in str(values[ptr])[:-2]][::-1]   # all leftmost digits (right-to-left) # rightmost is last param
    if  (opcode := int(str(values[ptr])[-2:])) == 99: break # two rightmost digits
    elif opcode == 1: values[vpos(3)] = values[vpos(1)] + values[vpos(2)]; ptr += 4
    elif opcode == 2: values[vpos(3)] = values[vpos(1)] * values[vpos(2)]; ptr += 4
    elif opcode == 3: values[vpos(1)] = int(input("Input (P5.5): ")); ptr += 2
    elif opcode == 4: output = values[vpos(1)]; ptr += 2
    elif opcode == 5: ptr = values[vpos(2)] if values[vpos(1)] != 0 else ptr+3
    elif opcode == 6: ptr = values[vpos(2)] if values[vpos(1)] == 0 else ptr+3
    elif opcode == 7: values[values[ptr+3]] = int(values[vpos(1)] <  values[vpos(2)]); ptr += 4
    elif opcode == 8: values[values[ptr+3]] = int(values[vpos(1)] == values[vpos(2)]); ptr += 4
  print(f"Puzzle 5.5: Intcode output: {output}")

############
# puzzle 6 #
############
## 6 ##
def puzzle6():
  with open('d6_input.txt', 'r') as f: orbits = [l.strip() for l in f.readlines()]
  # orbits = ["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L",]

  all_centers = {}
  for orbit in orbits:
    center,satellite = orbit.split(')') # each satellite will only appear once
    all_centers.setdefault(center, []).append(satellite)

  all_orbits = {c: {} for c in all_centers.keys()}

  for center, sats in all_centers.items():
    for satellite in sats:
      cur_COM = all_orbits[center].setdefault(satellite, {})
      while (cur_COM := cur_COM.setdefault(satellite, {})): pass

  for center, all_sats in all_orbits.items():
    for csat, sats in all_sats.items():
      all_orbits[center][csat] = all_orbits.get(csat, {})

  all_orbits = {'COM': all_orbits['COM']}

  def count(tree, num_levels_down=0):
    if not tree: return 0
    total_orbits = 0
    for center, planets_in_orbit in tree.items():
      cur_sub_orbits = count(planets_in_orbit, num_levels_down+1)
      total_orbits += num_levels_down + cur_sub_orbits
      # print(f"{center}, down: {num_levels_down}, {cur_sub_orbits=}, {total_orbits=}")
    return total_orbits

  total_orbits = count(all_orbits)
  print(f"Puzzle 6: Total direct+indirect orbits: {total_orbits}")

## 6.5 ##
def puzzle65():
  with open('d6_input.txt', 'r') as f: orbits = [l.strip() for l in f.readlines()]
  # orbits = ["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L","K)YOU","I)SAN",]

  m_orbits = list(map(lambda o: o.split(')'), orbits))
  all_centers = {center: [s for c,s in m_orbits if c == center] for center,sat in m_orbits}
  all_orbits = {c: {s: {} for s in s} for c,s in all_centers.items()}

  for center, all_sats in all_orbits.items():
    for csat, sats in all_sats.items():
      all_orbits[center][csat] = all_orbits.get(csat, {})

  def count(tree, num_levels_down=0):
    if not tree: return 0
    total_orbits = 0
    for center, planets_in_orbit in tree.items():
      cur_sub_orbits = count(planets_in_orbit, num_levels_down+1)
      total_orbits += num_levels_down + cur_sub_orbits
    return total_orbits

  def is_node_below(tree, key):
    if not tree: return False
    if key in tree.keys(): return True
    return any([is_node_below(t, key) for t in tree.values()])

  possibles = []
  for center, all_sats in all_orbits.items():
    if is_node_below(all_sats, 'YOU') and is_node_below(all_sats, 'SAN'):
      possibles.append({center: all_sats})

  def depth_of_node(tree, key, level=0):
    if not tree: return 0
    if key in tree: return level
    return sum([depth_of_node(t, key, level+1) for t in tree.values()])

  smallest_tree = sorted(possibles, key=lambda p: count(p))[0]
  smallest_tree = smallest_tree[list(smallest_tree.keys())[0]]

  num_transfers = depth_of_node(smallest_tree, 'YOU') + depth_of_node(smallest_tree, 'SAN')

  print(f"Puzzle 6.5: Minimum orbital transfers: {num_transfers}")

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
  # puzzle5()
  # puzzle55()
  puzzle6()
  puzzle65()
