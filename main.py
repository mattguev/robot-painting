from PIL import Image
from typing import List, Tuple
from dataclasses import dataclass, field
import random

from collections import deque
import numpy as np

@dataclass
class point:
    pt: Tuple[int,int]
    color: Tuple[int, int, int]
    dc: int # current distance to center -- used to make circles
    center: Tuple[int,int] # center from which a point is discovered

    # returns true if a center should be added to the queue valid neighbor
    def checksout(self, img: Image, proc: np.ndarray) -> bool:
        # want pt to be t1: in range (0 to w), t2: py in range 0 to h, t3: not processed
        x, y = self.pt
        t1 = x in range(img.width) # integer space
        t2 = y in range(img.height)
        t3 = False # available for processing
                    # need to set value for t3 before calling it again below

        if t1 and t2:
            t3 = not proc[x,y]
        return t1 and t2 and t3

    def dist(self,p1:Tuple[int,int],p2:Tuple[int,int])-> int: # Euclidean-ish distance
        return ((p1[0]-p2[0])*(p1[0]-p2[0])) + ((p1[1] - p2[1]) * (p1[1] - p2[1]))

    def neighbors(self):
        x, y = self.pt
        # define neighbors
        retneigh = [] # list of points
        neigh = [(x, y-1),(x-1,y-1),(x-1,y),(x-1,y+1),(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1)]
        for n in neigh:
            if self.dist(n,self.center) <= (self.dc+1)**2: # neighbor is within the next circle
                                            # self.dc + 1 indicates the next circle
                retneigh.append(point(n,self.color,self.dc+1,self.center))
        return retneigh


@dataclass
class centers:

    ctrs: List[point] = field(default_factory=list) # only data of centers class

    def __init__(self,img:Image, density: float): # constructor which gets called when you instantiate
        pixels = img.load() # pixels loaded from image into a variable (table of points)
        self.ctrs = []
        num_pixels = density * img.width * img.height
        for c in range(int(num_pixels)):
            x = random.randint(0, img.width-1)
            y = random.randint(0, img.height-1)
            self.ctrs.append(point((x,y),pixels[x,y],0,(x,y)))

# -------------------------------------------------------------------------------------------

# boilerplate for handling images in PIL
# open an image, create new centers, load the pixels we're setting
im = Image.open("parkPhoto.jpg")

center_points = centers(im, 0.1) # collection of centers

im_out = Image.new('RGB', (im.width,
                           im.height), (255, 255, 255))

pixels = im_out.load()

q = deque() # Using a deque because python has no queue!
processed = np.full((im_out.width, im_out.height), False) # GIVEN use numpy to make a boolean array used to mark progress
    # creates boolean map of pixels in our grid to indicate whether that pixel has been processed already.
    # End goal: all values in processed == True

# process and enqueue the centers
for c in center_points.ctrs:
    cx,cy = c.pt # give better names to the point of c.
    # mark as processed
    processed[cx,cy] = True
    # put color in right place on new image
    pixels[cx,cy] = c.color
    # enqueue center
    q.append(c) # deque's version of enqueue

while q:  # while queue is not empty
    # dequeue a point v
    v = q.popleft() # popleft is deque function

    for n in v.neighbors():
        if n.checksout(im, processed):
            nx, ny = n.pt # give better names to the point of n.
            # mark as processed
            processed[nx, ny] = True
            # put color in right place on new image
            pixels[nx, ny] = n.color
            # enqueue neighbor
            q.append(n) # deque's version of enque

im_out.save('vorPark.jpg')

