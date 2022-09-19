import re
import random

class State:
    def __init__(self, concern, possib, solved, pre_solved):
        self.concerned = concern
        self.possibility = possib
        self.solved = solved
        self.presolve = pre_solved

    def print_state(self):
        print("Concerned: " + str(self.concerned))
        print("Possibility: " + str(len(self.possibility)))
        print("Solved: " + self.solved)
        print("Presolve: " + self.presolve)
        print("")

def print_stack(stack):
    for state in reversed(stack):
        print("| Presolve: " + state.presolve + ", Solve: " + state.solved+ ", Length: " + str(len(state.possibility)) + ", Concerned Position: " + str(state.concerned) + " |")
    print("")
    
# Returns
def get_each_pos(input):
    map = {}

    for word in input:
        map[word] = [pos for pos, char in enumerate(input) if char == word]

    return list(map.values())

def get_lookup(mainDict):
    map = {}

    for word in mainDict:
        map[word] = get_each_pos(word)
    
    return map

def invert_lookup(lookup):
    map = {}

    for k, v in get_lookup(mainDict).items():
        v = str(v)
        map[v] = map.get(v, []) + [k]

    return map


# Main operations
def is_solved(input):
    for letter in input:
        if letter == '_':
            return False
    return True

def convert_to_unsolved(input):
    return re.sub('[a-zA-Z]', '_', input)

def apply_word(word, solved, pos):
    word_list = solved.split(" ")
    word_list[pos] = word

    return " ".join(word_list)

def smallest_entropys(solve_input, word_input, inverted):
    solve_list = solve_input.split(" ")
    word_list = word_input.split(" ")

    possible_list = []
    smallest_list = -1
    smallest_list_pos = -1

    for x in range(len(solve_list)):
        init_possible_list = inverted[str(get_each_pos(word_list[x]))]
        copy = init_possible_list[:]

        for possible in init_possible_list:
            if not matches_possible(solve_list[x], possible):
                copy.remove(possible)
        
        possible_list += [copy]

    for x in range(len(possible_list)):
        if smallest_list == -1:
            smallest_list = possible_list[x]
            smallest_list_pos = x
        elif len(possible_list[x]) == 1:
            continue
        elif len(possible_list[x]) < len(smallest_list):
            smallest_list = possible_list[x]
            smallest_list_pos = x

    return smallest_list_pos

# Checks if the input word matches the possible word
# Underscores in input represent unknown letters
# Eg: input: _ea_ should match with 'peak' and not 'held'
def matches_possible(input, possible):
    try:
        for x in range(len(input)):
            if input[x] != "_" and input[x] != possible[x]:
                return False
    except:
        print(input)
        print(possible)
        exit()
    return True

def get_possib(solve_input, word_input, inverted):
    solve_list = solve_input.split(" ")
    word_list = word_input.split(" ")

    possible_list = []

    #print("s: " + str(solve_list))
    #print("W: " + str(word_list))

    for x in range(len(word_list)):
        init_possible_list = inverted[str(get_each_pos(word_list[x]))]
        copy = init_possible_list[:]

        for possible in init_possible_list:
            if not matches_possible(solve_list[x], possible):
                copy.remove(possible)

        possible_list += [copy]

    return possible_list

def smallest(item):
    return len(item) if type(item)==list and len(item) > 1 else 999

def smallest_possib(posList):
    return posList.index(min(posList, key=smallest))

# Returns a list containing entropies of each word
def entropy(solve_input, word_input, inverted):
    possible_list = get_possib(solve_input, word_input, inverted)

    entropy_list = []

    for possible in possible_list:
        entropy_list.append(len(possible))
    
    return entropy_list

def smallest_entropy(solve_input, word_input, inverted):
    entropy_list = entropy(solve_input, word_input, inverted)

    smallest = 0
    pos = 0

    for val in range(len(entropy_list)):
        if val == 0:
            smallest = entropy_list[val]

        if entropy_list[val] == 1:
            continue

        if entropy_list[val] < smallest:
            smallest = entropy_list[val]
            pos = val
    
    return pos

def solve(solve_input, word_input):
    mapping_dict = {}

    letter_list = list(set(solve_input))

    for letter in letter_list:
        if letter == " " or letter == "_":
            continue

        mapping_dict[word_input[solve_input.index(letter)]] = letter

    solve_list = list(solve_input)

    for pos in range(len(solve_input)):
        if word_input[pos] == " ":
            solve_list[pos] = " "
        elif word_input[pos] in mapping_dict:
            solve_list[pos] = mapping_dict[word_input[pos]]
    
    solve_input = "".join(solve_list)
    
    return solve_input

# Checks if a sentence is valid
def is_valid(solve_input, word_input, inverted):
    entropy_list = entropy(solve_input, word_input, inverted)

    if 0 in entropy_list:
        return False
    return True

# Converts a regular english word into an encrypted word using the substitution cipher
def convert(word):
    word = str.lower(word)
    dictionary = {}
    count = 0
    new_word = ""

    for letter in word:
        if letter not in dictionary:
            if int(ord(letter)) not in range(97, 123) :
                if(letter == " "):
                    new_word += letter
                continue

            dictionary[letter] = chr(97 + count)
            count += 1
        
        new_word += dictionary[letter]  
        
    return new_word


if __name__ == "__main__":
    f = open('Cipher/Datasets/SmallWords.txt', 'r')

    mainDict = f.read().splitlines() 
    invertedMap = invert_lookup(mainDict)

    state_stack = []
    possibility_list= []

    generated = []
    required = 10


    backtrack_flag = False
    d_backtrack_flag = False

    # Get the word to solve
    deformed_word = convert(input("Enter the string: "))
    print("The word: " + deformed_word)

    solved_word = convert_to_unsolved(deformed_word)

    to_solve_word = ""

    deformed_list = deformed_word.split(" ")

    counter = 0

    reg = 0
    non = 0

    while(True):
        if backtrack_flag:
            print("Non regular run: " + str(non))
            non += 1 

            try:
                print("ending stack")
                print_stack(state_stack)
                this_state = state_stack.pop()
            except:
                print("")
                print("Finished")
                print(generated)
                exit()

            possibility_list = this_state.possibility
            solved_word = this_state.presolve
            word_pos = this_state.concerned

            backtrack_flag = False
        else:
            print("Regular run: " + str(reg))
            reg += 1
            # Get the position of the word with the lowest entroypy within the list

            # Get possibilities list
            # SUGGESTION: could improve performance by
            #   getting possibility list from smallest entropy call along with word pos 
            init_possib = get_possib(solved_word, deformed_word, invertedMap)
            word_pos = smallest_possib(init_possib)

            possibility_list = init_possib[word_pos]


        # Pick random word from possibilities
        random_word = random.choice(possibility_list)
        
        #print("Random word: "+ random_word)
        possibility_list.remove(random_word)

        # Push state onto stack
        prev_state = solved_word

        applied = apply_word(random_word, solved_word, word_pos)
        solved_word = solve(applied, deformed_word)

        print(random_word)
        print(applied)

        if len(possibility_list) == 0:
            print(len(possibility_list))
            if(is_solved(solved_word)):
                generated.append(solved_word)

            backtrack_flag = True
            continue
        else:
            new_state = State(word_pos, possibility_list, solved_word, prev_state)
            state_stack.append(new_state)
            
        if not is_valid(solved_word, deformed_word, invertedMap):
            print("not valid")
            backtrack_flag = True
        else:
            print("is valid")

        print_stack(state_stack)
        print("")

        if(is_solved(solved_word)):
            backtrack_flag = True
            counter += 1

            generated.append(solved_word)
        




