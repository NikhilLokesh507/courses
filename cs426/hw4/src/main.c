#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "kmeans.h"


#define TIMING
#define MAX_POINTS 151
#define DIM 3

int readData(const char* filename, float** points)
{
    FILE* df = fopen(filename, "r");
    if (!df) {
        fprintf(stderr, "File %s opening failed.\n", filename);
        exit(1);
    }
    char buf[128];
    int n_points = 0;
    float* pp;

    // discard header
    fgets(buf, sizeof(buf), df);

    while ((fgets(buf, sizeof(buf), df)) != NULL) {
        points[n_points] = (float*)malloc(DIM * sizeof(float));
        pp = points[n_points++];
        sscanf(buf, "%g,%g,%g", pp, pp+1, pp+2);
    }

    fclose(df);
    return n_points;
}

void writeResult(const char* filename, float** centroids, int K, int* c_idx, int n_points)
{
    FILE* file = fopen(filename, "w");
    if (!file) {
        fprintf(stderr, "File %s opening failed.\n", filename);
        exit(1);
    }


    // write centroids
    for (int ci = 0; ci < K; ++ci) {
        for (int di = 0; di < DIM; ++di)
            fprintf(file, "%f ", centroids[ci][di]);
        fprintf(file, "\n");
    }

    // write centroid id for each point
    for (int pi = 0; pi < n_points; ++pi)
        fprintf(file, "%d ", c_idx[pi]);

    printf("Write result to %s\n", filename);
}

void copy2D(float** dest, float** src, int d1, int d2)
{
    for (int ci = 0; ci < d1; ++ci)
        for (int di = 0; di < d2; ++di)
            dest[ci][di] = src[ci][di];
}

void freeCentroids(float** c, int K)
{
    for (int ci = 0; ci < K; ++ci)
        free(c[ci]);
    free(c);
}
int main(int argc, char* argv[])
{
    if (argc != 2 && argc != 3) {
        printf("Usage: %s K\n", argv[0]);
        printf("\t K        the number of clusters.\n");
        exit(1);
    }

    int K = atoi(argv[1]);
    float** points = (float**)malloc(MAX_POINTS * sizeof(float*));
    int n_points;

    if (argc == 3) {
        n_points = readData("data/data.csv", points);
    } else {
        n_points = readData(argv[2], points);
    }
    printf("Read %d points\n", n_points);

    int c_idx[n_points];

    clock_t start = clock();
    float** centroids = kmeans(points, n_points, DIM, K, 100, c_idx);
    float avg = avg_dist(points, n_points, DIM, centroids, K, c_idx);
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;

    printf("took %f seconds\n", seconds);
    printf("avg dist: %f\n", avg);

    char fn[20];
    sprintf(fn, "result/K-%d.out", K);
    writeResult(fn, centroids, K, c_idx, n_points);

    #ifdef TIMING
    seconds = 0;
    for (int i = 0; i < 500; ++i) {
        clock_t start = clock();
        float** c = kmeans(points, n_points, DIM, K, 100, c_idx);
        avg = avg_dist(points, n_points, DIM, c, K, c_idx);
        clock_t end = clock();
        seconds += (float)(end - start) / CLOCKS_PER_SEC;
        freeCentroids(c, K);
    }
    printf("kmeans time (500 round average): %f\n", seconds/500);
    #endif

    // free
    for (int pi = 0; pi < n_points; ++pi)
        free(points[pi]);
    free(points);

    freeCentroids(centroids, K);
}
