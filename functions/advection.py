from math import exp, sqrt, erfc

def StokesDrift(particle, fieldset, time):
    """Stokes drift kernel, following [Br16]_

    References
    ----------
    .. [Br16] Breivik et al. (https://doi.org/10.1016/j.ocemod.2016.01.005)
    """

    stokes_U = fieldset.Stokes_U[time, particle.depth, particle.lat, particle.lon]
    stokes_V = fieldset.Stokes_V[time, particle.depth, particle.lat, particle.lon]
    T_p = fieldset.wave_period[time, particle.depth, particle.lat, particle.lon]

    g = 9.81  # gravitational constant [m s-1]
    twopi = 2 * 3.141592653589793238462643383279502884197

    # Only compute displacements if the peak wave period is significant
    if T_p > 1E-14:
        omega_p = twopi / T_p           # Peak wave frequency
        k_p = (omega_p ** 2) / g        # Peak wave number

        kp_z_2 = 2. * k_p * particle.depth

        # Decay factor in Eq. (19) of [Br16]_
        decay = exp(-kp_z_2) - sqrt(.5 * twopi * kp_z_2) * erfc(sqrt(kp_z_2))

        # Apply Eq. (19) and compute particle displacement
        particle_dlon += stokes_U * decay * particle.dt
        particle_dlat += stokes_V * decay * particle.dt