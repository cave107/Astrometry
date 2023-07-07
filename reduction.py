import numpy as np
from collections import namedtuple

Star = namedtuple('Star', ['ra', 'dec', 'x', 'y'])

'''
reference_stars = [
    Star(210.551138, 54.526101, 1090, 960),
    Star(210.957632, 54.151411, 581, 156),
    Star(210.090241, 54.322905, 416, 525),
]
'''

reference_stars = [
    Star(210.351795, 54.364758, 1340.160000, 614.490000),
    Star(211.406949, 54.311582, 19.500000, 503.730000),
    Star(210.910511, 54.311722, 641.130000, 499.970000),
    Star(210.391781, 54.595120, 1287.810000, 1108.820000),
    Star(210.551225, 54.526081, 1089.890000, 959.960000),
    Star(210.957708, 54.151557, 580.910000, 156.310000),
    Star(211.090241, 54.322905, 416.200000, 524.940000),
    Star(210.238453, 54.469985, 1480.340000, 841.210000),
    Star(211.368388, 54.125551, 64.150000, 103.880000),
    Star(210.331405, 54.311089, 1366.300000, 499.400000)
]

reference_pixel = (750, 600) 

def linear_equation_system(b):
    A = np.ones((3, 3))
    A[:, 1:3] = np.array(reference_stars)[:, 2:4] - reference_pixel # subtract reference pixel from (x,y) of each reference star

    x = np.linalg.solve(A, b)

    return x

def interpolation():
    alpha_col = np.array(reference_stars)[:, 0]
    crval1, cd11, cd12 = linear_equation_system(alpha_col)
    
    delta_col = np.array(reference_stars)[:, 1]
    crval2, cd21, cd22 = linear_equation_system(delta_col)

    return crval1, cd11, cd12, crval2, cd21, cd22

def regression(stars, ref_px):
    m = len(stars)
    stars = np.array(stars)

    A = np.ones((m, 3))
    A[:, 1:3] = stars[:, 2:4] - ref_px

    Q, R = np.linalg.qr(A)

    ra = stars[:, [0]]
    y1 = (np.dot(Q.transpose(), ra))[:3]

    ra_coeffs = np.linalg.solve(R, y1)

    dec = stars[:, [1]]
    y2 = (np.dot(Q.transpose(), dec))[:3]

    dec_coeffs = np.linalg.solve(R, y2)

    return (*ra_coeffs, *dec_coeffs)
    

def main():
    '''
    crval1, cd11, cd12, crval2, cd21, cd22 = interpolation()
    print("Interpolation", crval1, crval2, cd11, cd12, cd21, cd22)
    '''

    crval1, cd11, cd12, crval2, cd21, cd22 = regression(reference_stars, reference_pixel)
    print("Regression", crval1, cd11, cd12, crval2, cd21, cd22)

if __name__ == '__main__':
    main()