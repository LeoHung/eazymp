from eazymp.atomic import Atomic
def iplusplus(num_round):
    global_i = 0 #pragma shared number
    for _ in range(num_round): #pragma omp parallel for
        for __ in range(5):
            with Atomic():
                global_i += 1
    return global_i

if __name__ == "__main__":
    print iplusplus(10)
