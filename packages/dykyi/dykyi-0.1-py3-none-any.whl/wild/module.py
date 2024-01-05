
def print_progress_bar(iteration, total, length=50):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '#' * filled_length + '-' * (length - filled_length)
    print(f'\rProgress: |{bar}| {percent}% Complete', end='\r')
    if iteration == total: 
        print()
