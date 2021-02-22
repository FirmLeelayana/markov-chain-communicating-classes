# markov-communicating-classes
Algorithm to find the highest length communicating class in a Markov-like chain problem.

The main idea was to use Markov Chain theory, specifically the idea of a class being all states that 'communicate' with one another.
A Markov transition matrix was initialised with 1's and 0's, and checked if the i,j and j,i positions were both 1. If so, they form part of a class. This loops over all states, separating them into different classes. Finally, to get the complete class, a state that were part of two different classes meant that these two classes actually form just one class, with that state connecting the two classes. This was done by extending the list of states in each class by their own respective class, and then eliminating redudancies in states (that appeared more than once). The maximum length class was found by finding the dictionary value with the largest length.
