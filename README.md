# robot-painting
Officially: an exercise in graph theory for data science purposes. 

Unofficially: my retribution and the culmination of a 12-year journey which unknowingly began when I almost failed Art in the 3rd grade because I couldn't paint a vase. 

Here, I provide an example of the famous use of Voronoi diagrams (https://plus.maths.org/content/maths-minute-voronoi-diagrams) in recreating the Pointillism style of art. The number of centers is determined by the user's desired density. From there, the algorithm colors each neighbor according to its closest center using a deque implementation which keeps runtime complexity to O(n). 
