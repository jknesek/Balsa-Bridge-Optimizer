def get_truss_efficiency(the_truss):
  weakest_load = 1000000.0
  for m in the_truss.members:
    if m.force > 0:
      supported_load = the_truss.load * m.fos_yielding / m.force
    else:
      if m.fos_yielding > m.fos_buckling:
        supported_load = the_truss.load * m.fos_yielding / m.force
      else:
        supported_load = the_truss.load * m.fos_buckling / m.force
    if supported_load < weakest_load:
        weakest_load = supported_load
  return weakest_load/the_truss.mass