# https://stackoverflow.com/a/19550879/8575847
def line_intersection(line1, line2):
  p0, p1 = line1
  p2, p3 = line2

  s10_x = p1[0] - p0[0]
  s10_y = p1[1] - p0[1]
  s32_x = p3[0] - p2[0]
  s32_y = p3[1] - p2[1]

  denom = s10_x * s32_y - s32_x * s10_y

  if denom == 0 : return None # collinear

  denom_is_positive = denom > 0

  s02_x = p0[0] - p2[0]
  s02_y = p0[1] - p2[1]

  s_numer = s10_x * s02_y - s10_y * s02_x
  t_numer = s32_x * s02_y - s32_y * s02_x

  if  (s_numer < 0) == denom_is_positive : return None # no collision
  if  (t_numer < 0) == denom_is_positive : return None # no collision
  if ((s_numer > denom) == denom_is_positive or
      (t_numer > denom) == denom_is_positive): return None # no collision

  # collision detected
  t = t_numer / denom
  intersection_point = [ int(p0[0] + (t * s10_x)), int(p0[1] + (t * s10_y)) ]

  return intersection_point

def manhattan(pt1, pt2):
  return abs(pt1[0]-pt2[0]) + abs(pt1[1]-pt2[1])