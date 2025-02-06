# In ursina/ursinamath.py, update the slerp function, it's for the map editor
from math import acos, sqrt, cos, sin, isclose

def slerp(v0, v1, t):
    costheta = max(min(dot(v0, v1), 1.0), -1.0)  # Clamp costheta between -1 and 1

    theta = acos(costheta)
    if isclose(theta, 0):
        return v0

    sin_theta = sin(theta)
    scale0 = sin((1 - t) * theta) / sin_theta
    scale1 = sin(t * theta) / sin_theta
    return (v0 * scale0) + (v1 * scale1)
