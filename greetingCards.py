# Name: Brandon Burdick
# Class: CPSC 535 Advanced Algorithms
# Assignment: Project 1
import re

# Function swaps the old string out for the new string by splitting string into 2, appending new string, and recombining them.
def string_change(string, old_str, new_str, index):
    first_part = string[0:index]
    second_part = string[index+len(old_str):len(string)]
    second_part = new_str + second_part
    return first_part + second_part

# Function used to uppercase characters at regex match, solving edge case swapped word wasn't capitalized and needs to be.
def uppercase_it(string, index, match):
    first_part = string[0:index]
    second_part = string[index+len(match):len(string)]
    second_part = match.upper() + second_part
    return first_part + second_part

#Main function
def main():

    # Prompt outputted to command line.
    print("Hello! Welcome to the greeting card fixer. Please enter the name of the .txt file")
    print("where your card message is stored. Then, the program will handle the rest.")
    print("=================================================================================")

    # Exception handling for improper file name input.
    while(True):
        filename = input("Please enter the name of the .txt file where your greeting card and requested swaps are stored: ")
        try:
            opened = open(filename, 'r').readlines()
        except FileNotFoundError:
            print("\nCouldn't find your file. Please make sure you type out the entire file name.")
            print("For example, if the file is named \"greetingcard.txt\" your input should be \"greetingcard.txt\"")
        else:
            break
 
    # Read through file and store values in their respective variable locations
    line_count = 0
    swaps = []
    with open(filename) as greeting:
        for line in greeting:
            line_count += 1
            if line_count == 1:
                message = (line.strip())
            if line_count > 1: 
                swaps.append(line.strip())

    # Split up our swaps list and store into a separate list called split_swaps
    split_swaps = []
    for swap in swaps:
        split_swaps.append(swap.split("# ")) #split() function breaks apart string at the # character, then appends it to the split_swaps list
    
    # list used to store information about the swaps index location in the message, as well as its corresponding index in the split_swaps list.
    swap_info = []

    # iterate across all words that are to be swapped to find all matches in string, 
    # then record the index of the match as well as the index of the string it correlates to.
    for i in range(len(split_swaps)):
        for match in re.finditer(split_swaps[i][0], message, re.IGNORECASE):   
            swap_index = []
            index = match.start()
            swap_index.append(split_swaps[i][0])
            swap_index.append(split_swaps[i][1])
            swap_index.append(index)
            swap_info.append(swap_index)

    # python lambda function to sort the swaps in reverse numerical order based on match index
    # sorted_swaps stores information in the form of: [['old str, 'new str', index_of_message]]
    sorted_swaps = sorted(swap_info, key=lambda x: x[2], reverse=True)
    for i in range(len(sorted_swaps)):
        message = string_change(message, sorted_swaps[i][0], sorted_swaps[i][1], sorted_swaps[i][2])

    # Because the finditer() can help to replace words that match with a lowercase version of it, i had to implement some regex
    # that verifies the replacement is the proper case when its the start of a sentence. i.e. , when house replaces Cars it becomes ". houses" 
    # but we want it to be -> ". Houses". Essentially this solves an edge case involved in this project.
    while(True):
        needs_upper = re.search("\. [a-z]", message)
        if (needs_upper):
            message = uppercase_it(message, needs_upper.start(), needs_upper.group())
        else: 
            break
    
    # Just some final output for the program.
    print("\n" + message + "\n")
    greetingcard = open("NewGreetingCard.txt", "w")
    greetingcard.write(message)
    greetingcard.close()
    print("Your new greeting card was saved to the file: NewGreetingCard.txt")
    
main()