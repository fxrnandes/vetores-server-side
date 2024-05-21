import random

def embaralhar_fisher_yates(vetor):
    n = len(vetor)
    for i in range(n - 1, 0, -1):
        j = random.randrange(i + 1)
        vetor[i], vetor[j] = vetor[j], vetor[i]
    return vetor
