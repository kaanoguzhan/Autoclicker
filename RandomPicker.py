import random


def rand_delayBefore(lastRand=0):
    rndmean = 0.71
    rnsigma = 0.123
    randmin = 0.3252412
    randmax = 1.0254214
    mindiffbefore = 0.09
    maxdiffbefore = 0.33
    randfnc = random.gauss

    rand = randfnc(rndmean, rnsigma)
    # Noise
    if random.randint(1, 10) == 1:
        if random.randint(1, 2) == 1:
            rand += random.uniform(mindiffbefore, maxdiffbefore)
        else:
            rand -= random.uniform(mindiffbefore, maxdiffbefore)
    # Ensuring withinh the bounds
    notInsideBounds = randmin > rand or rand > randmax
    # Ensuring not less than minimum diffbeforeerence
    notMindiffbefore = abs(rand - lastRand) < mindiffbefore
    # Ensuring not more than maximum diffbeforeerence
    notMaxdiffbefore = abs(rand - lastRand) > maxdiffbefore

    while notInsideBounds or notMindiffbefore or notMaxdiffbefore:
        rand = randfnc(rndmean, rnsigma)
        if random.randint(1, 10) == 1:
            if random.randint(1, 2) == 1:
                rand += random.uniform(mindiffbefore, maxdiffbefore)
            else:
                rand -= random.uniform(mindiffbefore, maxdiffbefore)
        notInsideBounds = randmin > rand or rand > randmax
        notMindiffbefore = abs(rand - lastRand) < mindiffbefore
        notMaxdiffbefore = abs(rand - lastRand) > maxdiffbefore

    return rand


def rand_delayBetween(lastRand=0):
    rndmean = 0.118
    rnsigma = 0.02
    randmin = 0.0728231
    randmax = 0.1856878
    mindiffbefore = 0.025
    maxdiffbefore = 0.080

    randfnc = random.gauss

    rand = randfnc(rndmean, rnsigma)
    if random.randint(1, 5) == 1:
        if rand < rndmean:
            rand += random.uniform(mindiffbefore, maxdiffbefore)
        elif rand > rndmean and random.randint(1, 3) == 1:
            rand -= random.uniform(mindiffbefore, maxdiffbefore)
    # Ensuring withinh the bounds
    notInsideBounds = randmin > rand or rand > randmax
    # Ensuring not less than minimum diffbeforeerence
    notMindiffbefore = abs(rand - lastRand) < mindiffbefore
    # Ensuring not more than maximum diffbeforeerence
    notMaxdiffbefore = abs(rand - lastRand) > maxdiffbefore

    while notInsideBounds or notMindiffbefore or notMaxdiffbefore:
        rand = randfnc(rndmean, rnsigma)
        if random.randint(1, 5) == 1:
            if rand < rndmean:
                rand += random.uniform(mindiffbefore, maxdiffbefore)
            elif rand > rndmean and random.randint(1, 3) == 1:
                rand -= random.uniform(mindiffbefore, maxdiffbefore)
        notInsideBounds = randmin > rand or rand > randmax
        notMindiffbefore = abs(rand - lastRand) < mindiffbefore
        notMaxdiffbefore = abs(rand - lastRand) > maxdiffbefore

    return rand
