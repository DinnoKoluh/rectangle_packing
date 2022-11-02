This project attempts to solve a variant of the *rectangle packing* problem. given a fixed-width plate and a list of rectangular circuits, decide how to place them on the plate so that the length of the final device is minimized Consider two variants of the problem. In the first, each 
circuit must be placed in a fixed orientation with respect to the others. This means that, an *n* × *m* circuit cannot be positioned as an *m* × *n* circuit in the silicon plate. In the second case, the rotation is allowed, which means that an *n* × *m* circuit can be positioned either as it is or as *m* × *n*.

There are three folders for each approach and in each one of them there is a README file to explain how to run the scripts. Each of the three
folders contains the following folders:
* figs  (contains figures of the solved instances (also the suboptimal ones) for the base model)
* figs_rots (contains figures of the solved instances (also the suboptimal ones) for the rotational model, with the keyword ROT on the
		     rectangles in the figures it is indicated which rectangles were rotated)
* instances (contains the instance files)
* out (contains the output .txt files for the base model (also the suboptimal solutions))
* out_rots (contains the output .txt files for rotational model (also the suboptimal solutions))
* src (contains the python scripts and function files)

This folder also contains the report file. 
In case of any problems please contact me.

<p align="left">
  <img alt="fig1" src="images\out-6.png" width="30%" />
  <img alt="fig2" src="images\out_rot-6.png" width="30%" />
</p>




