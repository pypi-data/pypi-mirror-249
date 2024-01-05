import pdb
import time
from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt


def pi_samples():
        '''Returns real space sample of momenta according to the distribution based on the modified kinetic term in the modified Hamiltonian.
        The sampling is easiest done in Fourier space and in terms of a real and hermitian object ``PI`` from which the momentum samples can be reconstructed (both in Fourier space) 
        The size of the lattice along one dimension L is assumed to be even.

        Returns
        -------
        pi: (L,L,3) array
            parameters for the sample of the conjugate momenta in real space
        '''
        pi_F = np.zeros((lattice_shape+(3,)), dtype=complex)
        # # momenta in Fourier space
        # pi_F = np.zeros((L, L, 3), dtype=complex)

        # PI_std = np.sqrt(L**2 / A) 
        # STD = np.repeat(PI_std[:,:,None], repeats=3, axis=2) # standard deviation is identical for components at same position
        # PI = np.random.normal(loc=0, scale=STD) #  (L,L,3) as returned array matches shape of STD

        # assign special modes for which FT exponential becomes +/-1. To get real pi in real space, the modes must be real themselves.
        N_2 = int(L/2)
        # two spacial indices
        pi_F[0,0] = PI[0,0]
        pi_F[0,N_2] = PI[0,N_2]
        pi_F[N_2,0] = PI[N_2,0]
        pi_F[N_2,N_2] = PI[N_2,N_2]

        # one special index
        pi_F[0,1:N_2] = 1/np.sqrt(2) * (PI[0,1:N_2] + 1j * PI[0,N_2+1:][::-1])
        pi_F[0,N_2+1:] = np.conj(pi_F[0,1:N_2][::-1]) # imposing hermitean symmetry

        pi_F[N_2,1:N_2] = 1/np.sqrt(2) * (PI[N_2,1:N_2] + 1j * PI[N_2,N_2+1:][::-1])
        pi_F[N_2,N_2+1:] = np.conj(pi_F[N_2,1:N_2][::-1])

        pi_F[1:N_2,0] = 1/np.sqrt(2) * (PI[1:N_2,0] + 1j * PI[N_2+1:,0][::-1])
        pi_F[N_2+1:,0] = np.conj(pi_F[1:N_2,0][::-1])

        pi_F[1:N_2,N_2] = 1/np.sqrt(2) * (PI[1:N_2,N_2] + 1j * PI[N_2+1:,N_2][::-1])
        pi_F[N_2+1:,N_2] = np.conj(pi_F[1:N_2,N_2][::-1])

        # no special index
        pi_F[1:N_2,1:N_2] = 1/np.sqrt(2) * (PI[1:N_2,1:N_2] + 1j * PI[N_2+1:,N_2+1:][::-1,::-1])
        pi_F[N_2+1:,N_2+1:] = np.conj(pi_F[1:N_2,1:N_2][::-1,::-1]) # imposing hermitean symmetry
   
        pi_F[1:N_2,N_2+1:] = 1/np.sqrt(2) * (PI[1:N_2,N_2+1:] + 1j * PI[N_2+1:,1:N_2][::-1,::-1])
        pi_F[N_2+1:,1:N_2] = np.conj(pi_F[1:N_2,N_2+1:][::-1,::-1])

        # pi is real by construction
        # pi = np.real(np.fft.ifft2(pi_F, axes=(0,1)))

        return pi_F


def pi_samples_for2():
    
    # momenta in Fourier space
    # pi_F = np.zeros((L, L, 3), dtype=complex)

    # PI_std = np.sqrt(L**2 / A) 
    # STD = np.repeat(PI_std[:,:,None], repeats=3, axis=2) # standard deviation is identical for components at same position
    # PI = np.random.normal(loc=0, scale=STD) #  (L,L,3) as returned array matches shape of STD
    pi_F = np.zeros((lattice_shape+(3,)), dtype=complex)


    for idx1 in range(L_2+1):
        for idx2 in range(L_2+1):
                # two special indices
                if ((idx1==0) or (idx1==L_2)) and ((idx2==0) or (idx2==L_2)): 
                    pi_F[idx1,idx2] = PI[idx1,idx2]
                    continue
                else:
                    pi_F[idx1,idx2] = 1/np.sqrt(2)*(PI[idx1,idx2] + 1j*PI[idx1,-idx2])

    # impose hermitian symmetry to get other entries
    pi_F_conj = np.conjugate(pi_F)

    for idx1 in range(L_2):
        for idx2 in range(L_2):
                pi_F[(L-idx1)%L,(L-idx2)%L] = pi_F_conj[idx1,idx2]

    # pi is real by construction
    # pi = np.real(np.fft.ifft2(pi_F, axes=(0,1)))

    return pi_F


def pi_samples_for3(pi_F, PI):
    
    # momenta in Fourier space
    # pi_F = np.zeros((L, L, 3), dtype=complex)

    # PI_std = np.sqrt(L**2 / A) 
    # STD = np.repeat(PI_std[:,:,None], repeats=3, axis=2) # standard deviation is identical for components at same position
    # PI = np.random.normal(loc=0, scale=STD) #  (L,L,3) as returned array matches shape of STD


    for idx1 in range(L_2+1):
        for idx2 in range(L_2+1):
            for idx3 in range(L_2+1):
                # two special indices
                if ((idx1==0) or (idx1==L_2)) and ((idx2==0) or (idx2==L_2)) and ((idx3==0) or (idx3==L_2)): 
                    pi_F[idx1,idx2,idx3] = PI[idx1,idx2,idx3]
                    continue
                else:
                    pi_F[idx1,idx2,idx3] = 1/np.sqrt(2)*(PI[idx1,idx2,idx3] + 1j*PI[idx1,-idx2,idx3])

    # impose hermitian symmetry to get other entries
    pi_F_conj = np.conjugate(pi_F)

    for idx1 in range(L_2):
        for idx2 in range(L_2):
            for idx3 in range(L_2):
                pi_F[(L-idx1)%L,(L-idx2)%L,(L-idx3)%L] = pi_F_conj[idx1,idx2,idx3]

    # pi is real by construction
    # pi = np.real(np.fft.ifft2(pi_F, axes=(0,1)))

    return pi_F





def pi_samples_while():
    '''
    Returns real space sample of momenta according to the distribution based on the modified kinetic term in the modified Hamiltonian.
    Due to the presence of the inverse kernel, the sampling is easiest done in Fourier space under the hermitian symmetry constraint to assure that the
    real space momenta are real-valued. From the 2L^D parameters (real and imaginary components at each site), this leaves L^D independent ones. These are 
    organised into the object ``PI`` and sampled from a Gaussian distribution. The Fourier space momentum samples are then reconstructed from ``PI``. 
    The size L of the lattice along one dimension is assumed to be even.

    Returns
    -------
    pi: (lattice shape,3) array
        parameters for the sample of the conjugate momenta in real space
    '''
    def get_special_points():
        '''
        Returns a list of all the coordinates (D-dimensional tuple) containing only the values 0 and L/2.
        '''
        all_special_points = np.full((2**D, D), np.nan)
        count = 0 # counts number of special points and used to index the above array
        # loop over number of L/2 occurances in special points 
        for num in range(0,D+1):
            aux = np.zeros(D, dtype='int')
            aux[:num] = L_2
            combs = list(set(permutations(aux)))
            for comb in combs:
                all_special_points[count] = np.array(comb)
                count += 1
        
        return all_special_points

    def hermitian_index(idx):
        '''
        returns the index of the hermitian conjugate pair of idx.
        '''
        idx_hconj = list(idx)
        for i,val in enumerate(idx):
              idx_hconj[i] = (L-val)%L
        
        return tuple(idx_hconj)
    
    def fill_pi_F(idx):
        '''
        Constructs the Foruier space momentum based on the Gaussian samples PI. 
        '''
        # special indices
        if np.prod(special_points==idx, axis=-1).any():
            idx = tuple(idx) # for correct indexing of ndarray
            pi_F[idx] = PI[idx]
        else: # non-special indices
            idx = tuple(idx)
            idx_her = hermitian_index(idx) 
            pi_F[idx] = 1/np.sqrt(2)*(PI[idx] + 1j*PI[idx_her])
            # pi_F[idx] = 1/np.sqrt(2)*(PI[idx_her] - 1j*PI[idx])
            # impose hermitian symmetry
            pi_F[idx_her] = np.conjugate(pi_F[idx])
    
    L_2 = int(L/2)

    pi_F = np.zeros((lattice_shape+(3,)), dtype=complex)

    PI_std = np.sqrt(L**D / A) 
    STD = np.repeat(PI_std[...,None], repeats=3, axis=-1) # standard deviation is identical for components at same position
    PI = np.random.normal(loc=0, scale=STD) # (lattice shape, 3) as returned array matches shape of STD
    
    # D nested for loops are simulated by storing the state of each counter in the vector idx. 
    # This also corresponds to the point in the Fourier space lattice for which pi_F is next computed.
    # The loop index 'k' indicates which loop is currently performed with 0 being the outer most one and D-1 the inner most one
    # The start and end index fields defined the initial and final configuration of the loop counter
    start = np.full(D, 0)
    idx = np.copy(start) 
    end = np.full(D, L)

    # list of points with all coorindates being 0 or L/2
    special_points = get_special_points()

    all_loops_done = False    
    while not all_loops_done:
        fill_pi_F(idx)
        k = D-1 # loop index
        while 1:
            idx[k] = idx[k] + 1 
            if idx[k] >= end[k]:
                if k == 0: # completed all loops
                    all_loops_done = True
                    break # break inner while and by setting flag to true outer one also terminates
                idx[k] = start[k]
                # move next most inner for loop one iteration forwards
                k -= 1
            else:
                break
             
    return pi_F

                

D = 2
L = 6
L_2 = int(L/2)
lattice_shape = tuple(np.repeat(L,D))

def kernel_inv_F():
    '''Finds inverse of the action kernel computed in the Fourier space, here referred to as ``A``.
    Does not exploit the symmetry of A, but the efficient computation via universal functions (ufuncs) yields a negligible
    run time even for large lattices.

    Returns
    -------
    A: (lattice shape) array
        inverse action kernel in Fourier space
    '''
    grid = np.indices(lattice_shape) # (D, lattice shape) ith array gives value of ith coordinate at each lattice site
    t = 4*np.sin(np.pi*grid/L)**2
    val = np.sum(t, axis=0) # (lattice shape)
    A = (val+0.1)**(-1)

    return A


A = kernel_inv_F()

np.random.seed(42)
pi_F = np.zeros((lattice_shape+(3,)), dtype=complex)

PI_std = np.sqrt(L**D / A) 
STD = np.repeat(PI_std[...,None], repeats=3, axis=-1) # standard deviation is identical for components at same position
PI = np.random.normal(loc=0, scale=STD) #  (L,L,3) as returned array matches shape of STD


a = pi_samples()
# b2 = pi_samples_for2()
# b3 = pi_samples_for3(pi_F,PI)
c = pi_samples_while()


print(np.allclose(a,c))
# print(np.imag(np.fft.ifft2(c, axes=(0,1))))
# print(a==c)
# print(np.allclose(b3,c))
# breakpoint()