# Pacman-Project-2 

### ***Question 1: Reflex Agent***

A simple evaluation function based on food's and ghosts' distances from pacman. The function computes all the distances from the successor position to food's positions. If there is food in the successor's position we motivate pacman to eat it by returning something (positive) big. If the minimum distance to ghost is 0 or 1 (meaning that if pacman choose this sucessor's position, the ghost will eat pacman in the next move or in two moves from now) we must prevent pacman from going there so we return something very small. In any other case, we return the opposite of the minimum food's distance. We choose to return the opposite number because the closest the food the better for pacman(we "convert" the small distance to a big return value, so to motivate pacman to move torwards the food).  

### ***Question 2: Minimax***

For this question we implement 3 functions:

1. getAction(): for every action in pacman's legal moves, call the min_value(), with depth=0 (first max level) and agent=1 (first min level). We compare all the values that min_value returns and pick the max. We return the action that led to max result.
2. max_value(): If we reach a terminal state we return the utility of the state. Else, for each action in pacman's legal moves we call the min_value(), with depth(same depth, depth changes everytime max is playing) and agent=1(first min after max). We return the max value.
3. min_value(): If we reach a terminal state we return the utility of the state. We check how many agents are left, since we can have many min agents consecutively. If we are in the last agent we must call the max_value and increase the depth by 1(depth increasing everytime max is playing). Else, we continue to the next agent(ghost) with min_value(). We return the min value.  

### ***Question 3: Alpha-Beta Pruning*** 

For this question we implement 3 functions:

1. getAction(): for every action in pacman's legal moves, call the min_value(), with a,b, depth=0 (first max level) and agent=1 (first min level). We compare all the values that min_value returns and pick the max(if the new returned value is greater than a, we set a to this value). We return the action that led to max result.
2. max_value(): If we reach a terminal state we return the utility of the state. Else, for each action in pacman's legal moves we call the min_value(), with depth(same depth, depth changes everytime max is playing) and agent=1(first min after max). If the returned value is greater than b(the instructions said to check only if it is greater not greater or equal), we return it. If the new returned value is greater than a, we set a to this value. We return the max value.
3. min_value(): If we reach a terminal state we return the utility of the state. We check how many agents are left, since we can have many min agents consecutively. If we are in the last agent we must call the max_value and increase the depth by 1(depth increasing everytime max is playing). Else, we continue to the next agent(ghost) with min_value(). If the returned value is less than a(the instructions said to check only if it is less not less or equal), we return it. If the new returned value is less than b, we set b to this value. We return the min value.  

### ***Question 4: Expectimax***  

For this question we implement 3 functions:

1. getAction(): for every action in pacman's legal moves, call the min_value(), with depth=0 (first max level) and agent=1 (first chance level). We compare all the values that chance_value returns and pick the max. We return the action that led to max result.
2. max_value(): If we reach a terminal state we return the utility of the state. Else, for each action in pacman's legal moves we call the chance_value(), with depth(same depth, depth changes everytime max is playing) and agent=1(first min after max). We return the max value.
3. chance_value(): If we reach a terminal state we return the utility of the state. We check how many agents are left, since we can have many min agents consecutively. If we are in the last agent we must call the max_value and increase the depth by 1(depth increasing everytime max is playing). Else, we continue to the next agent(ghost) with chance_value(). We sum the returned values.Finally, we return the average of all actions. (We assume in this exercise, that each action has the same propability).  

### ***Question 5: Better Evaluation Function***

An evaluation function based on:
1. *distance from food:* find the distances between pacman and available food. Keep the min distace. 
2. *number of food left:* the length of food list
3. *number of capsules left:* length of capsules list
4. *distance from scared ghosts:* find the distances between pacman and scared ghosts. Keep the min distace.
5. *distance from active ghosts:* find the distances between pacman and active ghosts. Keep the min distace.  

Importance of each evaluation factor:
1. *distance from food:* **-2** -> the closest the food the better for pacman, so we "convert" the small distance to a big return value, so to motivate pacman to move torwards the food.
2. *number of food left:* **-5** -> it is important for pamcan to eat all the food in the board, so the less remaining food the more important to eat it.
3. *number of capsules left:* **-25** -> eating capsules can be very beneficial for pacman, because he earns a lot of points and scares the ghosts. So we want him to eat them when he finds them, but not prefer them over close food, or running away from ghosts. 
4. *distance from scared ghosts:* **-3** -> it's beneficial for pacman to eat scared ghosts because he earns a lot of points, but we don't him to prefer eating one to eating food. 
5. *distance from active ghosts:* **-3 * 1/not_scared** -> we want pacman to stay away from ghosts. So we inverse the minimum distance to a ghost and multiply it with a negative number(the larger the distance the better for pacman).
Each time we sum all the evaluation factors and return a value.
