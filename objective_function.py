#!/usr/bin/python

"""
These objective functions are meant to be maximized. 
So, positive is better, 0 is neutral, negative is worse.

Parameter definitions:
CL: lift coefficient (2D), after dCL is applied (if applicable)
CL: drag coefficient (2D), after dCD is applied (if applicable)
dCL: change in CL (2D)
dCD: change in CD (2D)
AR: aspect ratio
eff: Oswalt efficiency factor
"""

import math

def objective_simple(dCL, dCD):
  return dCL - dCD

def induced_drag( CL, AR, eff ):
  CD3d = CL**2 / math.pi / AR / eff
  return CD3d

def lift3d( CL, AR ):
  CL3d = CL / ( 1 + CL / math.pi / AR )
  return CL3d

def objective_3d(dCL, dCD, CL, CD, AR, eff):
  CL3d = lift3d( CL, AR )
  CD3d = CD + induced_drag( CL, AR, eff )

  CL_now = CL - dCL
  CD_now = CD - dCD
  CL3d_now = lift3d( CL_now, AR )
  CD3d_now = CD_now + induced_drag( CL_now, AR, eff )

  dCL3d = CL3d - CL3d_now
  dCD3d = CD3d - CD3d_now
  return dCL3d - dCD3d

def objective(dCL, dCD, CL, CD):
  """
  This is simply an interfacial placeholder function.
  """
  AR = 5
  eff = 0.9
  return objective_3d(dCL, dCD, CL, CD, AR, eff)

if __name__ == "__main__":
  """
  This is mainly for testing purposes.
  """
  print "Welcome to the testing phase, we have fun and games."
  dCL = 0.1
  dCD = 0.03
  print "2D Objective: "+str(objective_simple(dCL,dCD))
  print "3D Objective: "+str(objective(0.1, 0.03, 2.5, 0.9))

