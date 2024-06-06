from darknet import *
from os import get_terminal_size


def print_in_columns(items:list[str], num_columns:int) -> None:
    items.reverse() # columns now read 1 - 150 top left to bottom right.
    
    screen_size = get_terminal_size()

    col_width = round(screen_size.columns / num_columns)
    
    grouped_items = [items[num:num+num_columns] for num in range(0, len(items), num_columns)]
    
    print('{: <col_width} {: <col_width} {: >col_width}'.format(*grouped_items))


        
if __name__  == "__main__":
    pass
