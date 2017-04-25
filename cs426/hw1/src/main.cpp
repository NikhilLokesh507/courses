#include <omp.h>
#include <cstdio>
#include <cstdlib>
#include <unistd.h>

#define NUM_THREADS 4
#define K 1000
double A[K][K], B[K][K], C1[K][K], C2[K][K]; // C = A * B

void init()
{
    int i, j;
#pragma omp parallel for private(j), num_threads(64)
    for (i = 0; i < K; i++)
        for (j = 0; j < K; j++) {
            A[i][j] = rand() * 1.0 / RAND_MAX;
            B[i][j] = rand() * 1.0 / RAND_MAX;
            C1[i][j] = 0;
            C2[i][j] = 0;
        }
}

int compareResult()
{
    int i, j;
    for (i = 0; i < K; i++)
        for (j = 0; j < K; j++)
            if (C1[i][j] != C2[i][j]) {
                return 0;
            }
    return 1;
}
void sequential()
{
    int i, j, k;
    for (i = 0; i < K; i++) {
        for (k = 0; k < K; k++) {
            for (j = 0; j < K; j++) {
                C1[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void parallel()
{
    int i, j, k;
#pragma omp parallel for private(j, k), num_threads(NUM_THREADS)
    for (i = 0; i < K; i++) {
        for (k = 0; k < K; k++) {
            for (j = 0; j < K; j++) {
                C2[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main()
{
    double start, end, stt = 0.0, ptt = 0.0;
    init();
    start = omp_get_wtime();
    sequential();
    end = omp_get_wtime();
    stt += end - start;

    start = omp_get_wtime();
    parallel();
    end = omp_get_wtime();
    ptt += end - start;

    printf("%f\n", stt);
    printf("%f\n", ptt);

    if (compareResult())
        printf("yes\n");
    else
        printf("no\n");
}
