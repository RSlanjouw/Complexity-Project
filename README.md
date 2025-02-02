# $\color{#0d0786}\text{Analysing Criminal Behaviour as a Complex System}$

This git-repo contains the Python files needed to get the simulations, plots and insight into crime spreading in an urban area using a continuous automaton (CA). For the transition function, we assume that neighborhoods with high crime negatively impact neighboring neighborhoods (increase the crime) and vice versa. The emergence of a giant component when varying teh influence difference is investigated and also the impact of police interference on this giant component. There is also research conducted into the possibility of the system having the property of self-organized criticality. 

### $\color{#7c06a7}\text{Purpose of the Research}$
We wanted to be able to create CA that could accurately depict the spread of crime in urban areas. We also wanted to find out if the broken window theory (BWT) is an example of self-organised criticality.

### $\color{#a42494}\text{Data}$
The transition function is based on the literature we found initially. It is given by: 

$$ C_{t+1} = \alpha C_t + \beta (1-\gamma) M + \frac{\beta}{2} L $$

where: 
- $C_{t+1}$ is the criminality value of a cell (neighborhood) in the next timestep,
- $\alpha$ and $\beta$ are parameters to determine how much the cell itself vs its neighbors affect the next criminiality value. $\alpha + \beta = 1$.
- $\gamma$ is a resistance to higher-criminality neighbors. This is based on education levels and income levels for each cell, which are uniform random distributions. $\gamma$ (as the average of the two) hence has a triangular distribution around $0.5$.
- $M$ is the average criminiality value of the neighboring cells with a higher criminality value.
- $L$ is the average criminality value of the neighboring cells with a lower criminality value
- If $M$ or $L$ is an empty set, the other part of the equation with $\beta$ is doubled.

This transition function succesfully creates clustering when starting with random criminality values for each neighborhood and causes spreading when starting iwtha  single neighborhood having criminality as per the BWT.

Please keep in mind that crime data in general have biases!

### $\color{#cf4e72}\text{Files}$
All files in the root are executables. In the modules function helper functions are placed which are used by the executables. The exploration folder contains files used to explore the system but are not used in the final plots. These files can be handy to better understand the system. These are not maintained. In the root is also a slide deck with info about our system. 

### $\color{#ec7c4c}\text{Conclusion}$
The experiments show that a giant component emerges when the influence of higher-criminality vs lower-criminality neighbors is investigated. This phase transition shows that a society's willingness to accept crime will affect whether crime will spread from local to more widespread and organised. Police interference also shifts the influence difference at which the giant component emerges, so that negative influence needs to weigh heavier. The experiemnts prove that the CA model is scale-free, as the giant component remains the same for different grid sizes and it also remains the same with police interference when the number of units remains proportional to the grid size.

However, the simulation does not exhibit a power law relationship and so the experiment cannot have the property of self-organised criticality.

### $\color{#facf28}\text{Group Members}$
Mika Doorenbosch,
Ruben Lanjouw, 
Liesbet Ooghe, 
Francesco Tiepolo
