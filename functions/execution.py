def DeleteErrorParticle(particle, fieldset, time):
    if particle.state >= 40:
        particle.delete()