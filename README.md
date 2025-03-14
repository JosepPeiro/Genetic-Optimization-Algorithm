# Genetic-Algorithm

## Author: Josep Peiró Ramos

This is the first developed optimization algorithm from an optional course of heuristic optimization carried out initiated by a professor from the Statistics and Operational Research department at the university of Valencia. This training course consisted of the development of an heuristic algorithm from the very beggining, i.e. programmed all by ourselves. This course was proposed only for the best students of the subject of Optimization.

We started this project on 20th of July of 2022, when I finished the first year of my degree.

This algorith solve a Knapsack problem (KP) with 2 backpacks with different (or same) weight. This problem consist in finding the best way for distributing a certain number of _products_, in a number of _backpacks_, where each product has a **_volume_** and a **_value_**; and each backpack has a **_capacity_**. And the target of this problem is maximizing the sum of values of this products, without the sum of the volumes of the products in each backpack exceeding its respective capacity.

The parameters of the problem has to be written in a txt file. With the next format:
- The first line must contain the capacities of each backpack (only 2 backpacks are allowed for this algorithm).
- The next lines are componed by the id of the object, the weight, and the value.
- Everything separated by semicolons (_";"_).

Example:

    350;430    
    1;35;72
    2;56;99
    3;110;226
    ...

The algorithm takes some time to arrive to a very good answer. It is a mainstream generic genetic algorithm for this Knapsack problem, so as they use to work, we create a certain number of solutions en each iteration. The family of solutions in one iteration is dependent of the iteration before, in other words, the solutions of one family will influence the next one, in terms that as that solution achieve a better objective value, they are more probable to keep _"alive"_ and to have mutations and combinations.
 
The parameters of the main function are: the limit in in seconds of the algorithm working (even though it is not well implemented), the numbers of solutions of the family in each iteration, the number of generations and the number of times the solution needs to decrease for deciding that we achieved the best solution 

Date of finishing 13/10/2022
