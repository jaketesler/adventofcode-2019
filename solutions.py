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
  def count(tree, num_levels_down=0): return sum([num_levels_down+count(planets_in_orbit, num_levels_down+1) for center, planets_in_orbit in tree.items()])
  # def count(tree, num_levels_down=0):
  #   return sum([
  #     num_levels_down+count(planets_in_orbit, num_levels_down+1)
  #     for center, planets_in_orbit in tree.items()
  #   ])
  orbits = tuple(map(lambda o: o.split(')'), orbits))
  all_orbits = {center: {s: {} for s in [sat for c,sat in orbits if c == center]} for center,_ in orbits}
  # all_orbits = {
  #   center: {
  #     s: {}
  #     for s in [
  #       sat
  #       for c,sat in orbits
  #       if c == center
  #     ]
  #   }
  #   for center,_ in orbits
  # }
  for center, all_sats in all_orbits.items(): all_orbits[center].update({sat: all_orbits.get(sat, {}) for sat in all_sats.keys()})
  # for center, all_sats in all_orbits.items():
  #   all_orbits[center].update(
  #     {
  #       sat: all_orbits.get(sat, {})
  #       for sat in all_sats.keys()
  #     }
  #   )
  total_orbits = count({'COM': all_orbits['COM']})
  print(f"Puzzle 6: Total direct+indirect orbits: {total_orbits}")

## 6.5 ##
def puzzle65():
  with open('d6_input.txt', 'r') as f: orbits = [l.strip() for l in f.readlines()]
  def count(tree, num_levels_down=0): return sum([num_levels_down+count(planets_in_orbit, num_levels_down+1) for center, planets_in_orbit in tree.items()])
  def depth_of_node(tree, key, level=0): return level if key in tree else sum([depth_of_node(t, key, level+1) for t in tree.values()])
  # def depth_of_node(tree, key, level=0):
  #   return level if key in tree else sum(
  #     [
  #       depth_of_node(t, key, level+1)
  #       for t in tree.values()
  #     ]
  #   )
  orbits = tuple(map(lambda o: o.split(')'), orbits))
  all_orbits = {center: {s: {} for s in [sat for c,sat in orbits if c == center]} for center,_ in orbits}
  for center, all_sats in all_orbits.items(): all_orbits[center].update({sat: all_orbits.get(sat, {}) for sat in all_sats.keys()})
  smallest_tree = tuple(min([{center: all_sats} for center, all_sats in all_orbits.items() if depth_of_node(all_sats, 'YOU') and depth_of_node(all_sats, 'SAN')], key=lambda p: count(p)).values())[0]
  # smallest_tree = tuple(
  #   min(
  #     [
  #       {center: all_sats}
  #       for center, all_sats in all_orbits.items()
  #       if depth_of_node(all_sats, 'YOU') and depth_of_node(all_sats, 'SAN')
  #     ], key=lambda p: count(p)
  #   ).values()
  # )[0]
  min_transfers = depth_of_node(smallest_tree, 'YOU') + depth_of_node(smallest_tree, 'SAN')
  print(f"Puzzle 6.5: Minimum orbital transfers: {min_transfers}")

############
# puzzle 7 #
############
## 7 ##
def puzzle7():
  def intcode(inputs): # two inputs expected
    with open('d7_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
    vpos = lambda m_idx: values[ptr+m_idx] if get(modes, m_idx-1, 0) == 0 else ptr+m_idx # given a mode index, calculate the proper position for indexing into values
    ptr = 0
    output = 0
    inputs = (x for x in inputs)
    while ptr < len(values):
      modes = [int(c) for c in str(values[ptr])[:-2]][::-1]   # all leftmost digits (right-to-left) # rightmost is last param
      if  (opcode := int(str(values[ptr])[-2:])) == 99: break # two rightmost digits
      elif opcode == 1: values[vpos(3)] = values[vpos(1)] + values[vpos(2)]; ptr += 4
      elif opcode == 2: values[vpos(3)] = values[vpos(1)] * values[vpos(2)]; ptr += 4
      elif opcode == 3: values[vpos(1)] = next(inputs); ptr += 2 # input signal
      elif opcode == 4: output = values[vpos(1)]; ptr += 2
      elif opcode == 5: ptr = values[vpos(2)] if values[vpos(1)] != 0 else ptr+3
      elif opcode == 6: ptr = values[vpos(2)] if values[vpos(1)] == 0 else ptr+3
      elif opcode == 7: values[values[ptr+3]] = int(values[vpos(1)] <  values[vpos(2)]); ptr += 4
      elif opcode == 8: values[values[ptr+3]] = int(values[vpos(1)] == values[vpos(2)]); ptr += 4
    return output

  signals = {}
  for phase in itertools.permutations(range(5)):
    phase_ = "".join((str(n) for n in phase))
    outA = intcode((phase[0], 0))
    outB = intcode((phase[1], outA))
    outC = intcode((phase[2], outB))
    outD = intcode((phase[3], outC))
    outE = intcode((phase[4], outD))
    signals[phase_] = outE

  print(f"Puzzle 7: Maximum thruster signal: {max(signals.values())}")

from queue import Queue
from threading import Thread
## 7.5 ##
def puzzle75():
  def intcode(input_queue, output_queue): # two inputs expected
    with open('d7_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]

    vpos = lambda m_idx: values[ptr+m_idx] if get(modes, m_idx-1, 0) == 0 else ptr+m_idx # given a mode index, calculate the proper position for indexing into values
    ptr = 0
    output = 0
    done = False
    while ptr < len(values):
      modes = [int(c) for c in str(values[ptr])[:-2]][::-1]   # all leftmost digits (right-to-left) # rightmost is last param
      if  (opcode := int(str(values[ptr])[-2:])) == 99: done = True; break # two rightmost digits
      elif opcode == 1: values[vpos(3)] = values[vpos(1)] + values[vpos(2)]; ptr += 4
      elif opcode == 2: values[vpos(3)] = values[vpos(1)] * values[vpos(2)]; ptr += 4


      elif opcode == 3:
        try:
          values[vpos(1)] = input_queue.get()
        except:
          values[vpos(1)] = output_queue.get(timeout=3)
        ptr += 2 # input signal

      elif opcode == 4:
        output = values[vpos(1)]
        output_queue.put(output)
        ptr += 2
      elif opcode == 5: ptr = values[vpos(2)] if values[vpos(1)] != 0 else ptr+3
      elif opcode == 6: ptr = values[vpos(2)] if values[vpos(1)] == 0 else ptr+3
      elif opcode == 7: values[values[ptr+3]] = int(values[vpos(1)] <  values[vpos(2)]); ptr += 4
      elif opcode == 8: values[values[ptr+3]] = int(values[vpos(1)] == values[vpos(2)]); ptr += 4
    return

  signals = {}
  for phase in itertools.permutations(range(5,10)):
    inToA = Queue(); inToA.put(phase[0]); inToA.put(0)
    inToB = Queue(); inToB.put(phase[1])
    inToC = Queue(); inToC.put(phase[2])
    inToD = Queue(); inToD.put(phase[3])
    inToE = Queue(); inToE.put(phase[4])

    outToB = inToB
    outToC = inToC
    outToD = inToD
    outToE = inToE
    outToA = inToA

    tA = Thread(target=intcode, args=(inToA, outToB))
    tB = Thread(target=intcode, args=(inToB, outToC))
    tC = Thread(target=intcode, args=(inToC, outToD))
    tD = Thread(target=intcode, args=(inToD, outToE))
    tE = Thread(target=intcode, args=(inToE, outToA))

    tA.start(); tB.start(); tC.start(); tD.start(); tE.start()
    tA.join(); tB.join(); tC.join(); tD.join(); tE.join()

    phase_ = "".join((str(n) for n in phase))
    signals[phase_] = outToA.get(timeout=3)

  print(f"Puzzle 7.5: Maximum feedback thruster signal: {max(signals.values())}")

############
# puzzle 8 #
############
## 8 ##
def puzzle8():
  with open('d8_input.txt', 'r') as f: values = [int(l) for l in f.readlines()[0].strip()]
  # image dims: 25px x 6px x NUM_LAYERS
  num_layers = int(len(values) / (25*6))
  pixel_sums_per_layer = []
  layers = []
  for layer in range(0, num_layers):
    layers.append(values[25*6*layer:25*6*(layer+1)])

  fewest_0s_layer = (0, 999) # idx, count
  for idx, layer in enumerate(layers):
    num_0s = 0
    for px in layer:
      if px == 0: num_0s += 1
    if fewest_0s_layer[1] > num_0s:
      fewest_0s_layer = (idx, num_0s)

  num_ones = num_twos = 0
  for px in layers[fewest_0s_layer[0]]:
    if px == 1: num_ones += 1
    if px == 2: num_twos += 1

  print(f"Puzzle 8: 1s X 2s: {num_ones * num_twos}")

## 8.5 ##
def puzzle85():
  # image dims: 25px x 6px x NUM_LAYERS
  with open('d8_input.txt', 'r') as f: values = [int(l) for l in f.readlines()[0].strip()]
  width, height = (25, 6)

  num_layers = int(len(values) / (width*height))
  pixel_sums_per_layer = []
  layers = []
  for layer in range(0, num_layers): layers.append(values[width*height*layer:width*height*(layer+1)])

  image = layers[0][:]
  for layer in layers[1:]:
    for idx, px in enumerate(layer):
      if image[idx] == 2: image[idx] = px # transparent -> replace

  image_out = [[], [], [], [], [], []]
  for h in range(height):
    for w in range(width):
      image_out[h].append(image[(width*h)+w])
    image_out[h] = "".join('X' if p else '-' for p in image_out[h])

  print("Puzzle 8.5: Image contents: \n{}".format('\n'.join(image_out)))

############
# puzzle 9 #
############
## 9 ##
def puzzle9():
  with open('d9_input.txt', 'r') as f: values = [int(v) for v in f.readlines()[0].strip().split(',')]
  # values = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
  # values = [1102,34915192,34915192,7,4,7,99,0]
  # values = [104,1125899906842624,99]
  values = {idx: val for idx,val in enumerate(values)}
  def vpos(m_idx): # given a mode index, calculate the proper position for indexing into values
    m = get(modes, m_idx-1, 0)
    if   m == 1: return ptr+m_idx                    # immediate mode
    elif m == 0: return values[ptr+m_idx]            # position mode
    elif m == 2: return values[ptr+m_idx] + rel_base # relative mode

  ptr = 0
  rel_base = 0
  output = []
  while ptr < len(values.keys()):
    modes = [int(c) for c in str(values[ptr])[:-2]][::-1]   # all leftmost digits (right-to-left) # rightmost is last param
    if  (opcode := int(str(values[ptr])[-2:])) == 99: break # two rightmost digits
    elif opcode == 1: values[vpos(3)] = values.setdefault(vpos(1), 0) + values.setdefault(vpos(2), 0); ptr += 4
    elif opcode == 2: values[vpos(3)] = values.setdefault(vpos(1), 0) * values.setdefault(vpos(2), 0); ptr += 4
    elif opcode == 3: values[vpos(1)] = int(input("Input (9): ")); ptr += 2
    elif opcode == 4: output.append(values.setdefault(vpos(1), 0)); ptr += 2
    elif opcode == 5: ptr = values.setdefault(vpos(2), 0) if values.setdefault(vpos(1), 0) != 0 else ptr+3
    elif opcode == 6: ptr = values.setdefault(vpos(2), 0) if values.setdefault(vpos(1), 0) == 0 else ptr+3
    elif opcode == 7: values[vpos(3)] = int(values.setdefault(vpos(1), 0) <  values.setdefault(vpos(2), 0)); ptr += 4
    elif opcode == 8: values[vpos(3)] = int(values.setdefault(vpos(1), 0) == values.setdefault(vpos(2), 0)); ptr += 4
    elif opcode == 9: rel_base += values.setdefault(vpos(1), 0); ptr += 2
  print(f"Puzzle 9: Intcode output: {output}")


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
  # puzzle6()
  # puzzle65()
  # puzzle7()
  # puzzle75()
  # puzzle8()
  # puzzle85()
  puzzle9()
