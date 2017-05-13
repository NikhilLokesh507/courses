#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "kmeans.h"

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

int main(int argc, char* argv[])
{
    if (argc != 2) {
        printf("Usage: %s K\n", argv[0]);
        printf("\t K        the number of clusters.\n");
        exit(1);
    }

    int K = atoi(argv[1]);
    float** points = (float**)malloc(MAX_POINTS * sizeof(float*));
    int n_points;
    n_points = readData("data/data.csv", points);
    printf("Read %d points\n", n_points);

    int c_idx[n_points];
    float** centroids = kmeans(points, n_points, DIM, K, 100, c_idx);
    char fn[20];
    sprintf(fn, "result/K-%d.out", K);
    writeResult(fn, centroids, K, c_idx, n_points);

    // free
    for (int pi = 0; pi < n_points; ++pi)
        free(points[pi]);
    free(points);

    for (int ci = 0; ci < K; ++ci)
        free(centroids[ci]);
    free(centroids);
}
