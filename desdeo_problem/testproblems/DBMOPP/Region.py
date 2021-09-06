from utilities import *
from typing import Dict, Tuple
import numpy as np
from time import time
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from numpy import matlib # i guess we could implement repmat ourselves
from desdeo_problem.problem import *
from matplotlib import cm

# utilities
# TODO: figure out the structure

class Attractor:
    def __init__(self) -> None:
        self._locations = None
    
    @property
    def locations(self):
        return self._locations

    @locations.setter
    def locations(self, value):
        self._locations = value
    
    def get_minimum_distance(self, x):
        d = euclidean_distance(self.locations, x)
        return np.min(d)

class Region:
    def __init__(self, centre: np.ndarray = None, radius: float = None):
        self._centre = centre
        self._radius = radius
    
    @property
    def centre(self):
        return self._centre

    @centre.setter
    def centre(self, value):
        self._centre = value

    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = value
    
    def is_close(self, x:np.ndarray, eps = 1e-06):
        return self.radius + eps > self.get_distance(x)
    
    def is_inside(self, x:np.ndarray, include_boundary = False):
        if include_boundary:
            return self.get_distance(x) <= self.radius
        return self.get_distance(x) < self.radius 
    
    def get_distance(self, x: np.ndarray):
        return euclidean_distance(self.centre, x)
    
    def calc_location(self, a, rotation): # this is also used in place attractors. so maybe move this so it's also accesible from there
        radiis = matlib.repmat(self.radius, 1, 2)
        return (
            self.centre + radiis
            * np.hstack((
                np.cos(a + rotation),
                np.sin(a + rotation)
            ))
        )
    
    def plot(self, color, ax):
        x = self.centre[0]
        y = self.centre[1]
        circle = Circle((x,y), self.radius, fc = color, fill = True, alpha = 0.5)
        ax.add_patch(circle)
    
class AttractorRegion(Region):
    def __init__(self, locations, indices, centre, radius, convhull):
        self.locations = locations
        self.objective_indices = indices
        super().__init__(centre, radius)
        self.convhull = convhull 
    
    def in_hull(self, x):
        if isinstance(self.convhull, ConvexHull):
            return in_hull(x, self.convhull.simplices)
        else:
            if self.locations.shape[0] == 1:
                return self.locations == x
            else:
                pass
                #check if between 2 points

    def plot(self, ax, color = 'b'):
        """

        """
        if self.convhull is None: return

        p = np.atleast_2d(self.locations)

        if not isinstance(self.convhull, ConvexHull):
            if p.shape[0] == 1:
                ax.scatter(self.locations[:,0], self.locations[:,1], color=color)
            else:
                ax.plot(self.locations[:,0], self.locations[:,1], color=color)
        else:
            for i, s in enumerate(self.convhull.simplices):
                ax.plot(p[s,0], p[s,1], color = 'black') # outline

                # add points
                ax.scatter(p[i,0], p[i,1], color = 'blue')
                ax.annotate(i, (p[i,0], p[i,1]))
            
            ax.fill(p[self.convhull.vertices, 0], p[self.convhull.vertices, 1], color=color, alpha = 0.7)

