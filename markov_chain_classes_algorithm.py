import numpy as np 
import copy
import sys

def readText(filename):
    '''
    Args:
    filename = path to text file
    
    Returns:
    markov_matrix = a n x n numpy matrix with 1, representing a pseudo markov transition matrix, where a 1 represents 
                    a player i (row i) being able to see player j (col j)
    d = dictionary with keys being the player's names and associated values are integers 0....n (assigning each player
        a value from 0 onwards)
    player_number = integer overall number of players
    '''
    
    d = {}
    player_number = 0

    with open(filename, 'r') as reader: #opening file
        for line in reader.readlines(): #reading each line in the file
            result = [x.strip() for x in line.split(',')] #removing comma and whitespaces
            if result[0] in d:
                raise ValueError('Text file not in supported format. Initial player name per row can only occur once throughout.')
            d[result[0]] = player_number #creating dictionary for all players, assigning each player a value from 0 onwards
            player_number+=1 #to calculate number of players

        #create markov transition matrix: 1 if player (the row) can see the other player (the column), 0 if cannot
        markov_matrix = np.zeros((player_number,player_number))  

    with open(filename, 'r') as reader: #opening file
        for line in reader.readlines(): #reading each line in the file
            result = [x.strip() for x in line.split(',')] #removing comma and whitespaces
            
            if player_number == 1: #accounting for the 1 player case
                markov_matrix[0][0] = 1
                break
            
            for player in result[1:]: #going through all players seen by player x
                current_player = result[0] #current player we are focusing on
                other_seen_players = player #players seen by that current_player
                markov_matrix[d[current_player]][d[other_seen_players]] = 1 #set value to 1 if the current player can see the other player
    
    return markov_matrix, d, player_number

def findCommunicatingClasses(d, markov_matrix, player_number):
    '''
    Args: 
    markov_matrix = a n x n numpy matrix with 1, representing a pseudo markov transition matrix, where a 1 represents 
                    a player i (row i) being able to see player j (col j)
    d = dictionary with keys being the player's names and associated values are integers 0....n (assigning each player
        a value from 0 onwards)
    player_number = integer overall number of players
    
    Returns:
    d2 = dictionary, with key being player name, and associated values being a list of the players that 'communicate' with each 
        other in Markov Chain terms, i.e. the two players can see each other
    '''
    
    d2 = {y: [] for y in d} #creating a dictionary with key being player names, and values being empty list
    inv_map = {v: k for k, v in d.items()} #creating an inverse of d for use later
    for i in range(player_number): #iterating over player i
        for j in range(player_number): #iterating over player j
            if markov_matrix[i][j] * markov_matrix[j][i] > 0: #the two values in the matrix must both be 1 if they are both able to see one another
                pl_name = inv_map[i] 
                d2[pl_name].append(inv_map[j]) #append this player to the dictionary

    return d2

def fullCommClasses(d2):
    '''
    Arg:
    d2 = dictionary, with key being player name, and associated values being a list of the players that 'communicate' with each 
        other in Markov Chain terms, i.e. the two players can see each other
        
    Returns:
    d3 = dictionary, with key being player name, and values being the full list of players that represent
         communicating classes for that player, including the player itself
    '''
    d3 = copy.deepcopy(d2) #create a deep copy of the dictionary

    for key, player_list in d2.items(): #iterating over the players
        if player_list: #if list is not empty
            for val in player_list: 
                if d3[key]: #if list is not empty
                    d3[key].extend(d3[val]) #extending the d3 dictionary values (list of player names)
                    d3[key] = list(set(d3[key])) #converting to set then list to eliminate redundancies
                elif not d3[key]:
                    d3[key] = list(set(d3[val]))
        
    return d3

def findMaximumLengthClass(d3):
    '''
    Arg:
    d3 = dictionary, with key being player name, and values being the full list of players that represent
         communicating classes for that player, including the player itself
         
    Returns:
    maximum = the maximum length of any communicating class in the Markov Chain
    '''
    d4 = {key: set(value) for key, value in d3.items()} #creating new dictionary that converts list to set instead to eliminate redundancies
    maximum = 1 #set initial value for maximum
    for key, value in d4.items(): #finding maximum length class
        length_key = len(value)
        if length_key > maximum:
            maximum = length_key
    return maximum

def markovModelSolution(filename):
    '''
    Arg:
    filename = text file name
         
    Returns:
    maximum = the maximum length of any communicating class in the Markov Chain
    '''
    markov_matrix, d, player_number = readText(filename)
    d2 = findCommunicatingClasses(d, markov_matrix, player_number)
    d3 = fullCommClasses(d2)
    maximum = findMaximumLengthClass(d3) 
    return maximum

if __name__ == "__main__":
    try:
        txtfile = sys.argv[1]
        if type(txtfile) != str or not txtfile.endswith('.txt'):
            raise TypeError("The supplied file is not supported. Please enter the name of a text file, ending with '.txt'") #tests for correct format
        else:
            solution = markovModelSolution(txtfile)
            print(f'Maximum number of players that can touch a single ball is: {solution} number of player(s).')
    except IndexError:
        print("Please supply a valid text file name.")
    
