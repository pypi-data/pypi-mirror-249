import random 


def return_random_number(lower_bound: int = 0, 
                         upper_bound: int = 6):
    return random.randint(lower_bound, upper_bound)

def return_random_list(lower_bound: int = 0, 
                       upper_bound: int = 6):
    return [return_random_number(lower_bound, upper_bound) for _ in return_random_number(lower_bound, upper_bound)]

def return_random_dict(lower_bound: int = 0, 
                       upper_bound: int = 6):
    return {return_random_number(lower_bound, upper_bound): return_random_number(lower_bound, upper_bound) for _ in return_random_number(lower_bound, upper_bound)}

def return_random_set(lower_bound: int = 0, 
                       upper_bound: int = 6):
    return {return_random_number(lower_bound, upper_bound) for _ in return_random_number(lower_bound, upper_bound)}

...
    