import numpy as np


def MatrixT(p0, K, p0_, p1_, p2_, p3_):
    x0, y0 = p0
    x1, y1 = (x0+K, y0)
    x2, y2 = (x0+K, y0+K)
    x3, y3 = (x0, y0+K)

    u0, v0 = p0_
    u1, v1 = p1_
    u2, v2 = p2_
    u3, v3 = p3_

    A = np.array(
        [[x0, y0,  1,  0,  0, 0, -x0*u0, -y0*u0],
         [x1, y1,  1,  0,  0, 0, -x1*u1, -y1*u1],
         [x2, y2,  1,  0,  0, 0, -x2*u2, -y2*u2],
         [x3, y3,  1,  0,  0, 0, -x3*u3, -y3*u3],
         [0,  0,  0, x0, y0, 1, -x0*v0, -y0*v0],
         [0,  0,  0, x1, y1, 1, -x1*v1, -y1*v1],
         [0,  0,  0, x2, y2, 1, -x2*v2, -y2*v2],
         [0,  0,  0, x3, y3, 1, -x3*v3, -y3*v3]]
    )

    b = np.array([u0, u1, u2, u3, v0, v1, v2, v3])

    c = np.linalg.solve(A, b)

    return c
