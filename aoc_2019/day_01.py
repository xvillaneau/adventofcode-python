def fuel_required(mass: int):
    return mass // 3 - 2

def sum_fuel(modules):
    return sum(map(fuel_required, modules))

def adjusted_fuel(mass: int):
    fuel, mass = 0, fuel_required(mass)
    while mass > 0:
        fuel += mass
        mass = fuel_required(mass)
    return fuel

def sum_adjusted(modules):
    return sum(map(adjusted_fuel, modules))

if __name__ == '__main__':
    from libaoc import files, simple_main
    simple_main(2019, 1, files.read_int_list, sum_fuel, sum_adjusted)
