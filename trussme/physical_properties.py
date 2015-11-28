# Gravitational constant for computing weight from mass
g = 9.80665


# Material properties
materials = {"A36":     {"rho": 7800,
                         "E":   200*pow(10, 9),
                         "Fy":  250*pow(10, 6),
                         "Cy":  250*pow(10, 6)},
             "A992":    {"rho": 7800,
                         "E":   200*pow(10, 9),
                         "Fy":  345*pow(10, 6),
                         "Cy":  345*pow(10, 6)},
             "BALSA":   {"rho": 150,
                         "E":   3.7*pow(10, 9),
                         "Fy":  20*pow(10, 6),
                         "Cy":  12*pow(10, 6)}, # compression strength is different that yeild strength for wood
             "IDEAL":   {"rho": 1*pow(10, -15), # super light
                         "E":   1*pow(10, 15),  # extremely rigid
                         "Fy":  1*pow(10, 15),
                         "Cy":  1*pow(10, 15)}, # damned hard to rupture
             "6061_T6": {"rho": 2700,
                         "E":   68.9*pow(10, 9),
                         "Fy":  276*pow(10, 6),
                         "Cy":  276*pow(10, 6)}}


# Checks to see if material name is valid
def valid_member_name(name):
    if name in materials.keys():
        return True
    else:
        return False