#include "kmeans.h"
#include <float.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

void print(float** a, int r, int c)
{
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; ++j) {
            printf("%f ", a[i][j]);
        }
        puts("\n");
    }
}


float dist2(float* p1, float* p2, int n_dim)
{
    float d = 0;
    for (int i = 0; i < n_dim; ++i) {
        d += (*p1 - *p2) * (*p1 - *p2);
        ++p1;
        ++p2;
    }
    return d;
}

int find_closest(float** points, int n_points, int n_dim, float** centroids, int K, int* c_idx)
{
    float mindist, dist, idx = 0;
    int unchanged = 1;
    for (int pi = 0; pi < n_points; ++pi) {
        mindist = FLT_MAX;

        for (int ci = 0; ci < K; ++ci) {
            dist = dist2(points[pi], centroids[ci], n_dim);
            if (dist < mindist) {
                mindist = dist;
                idx = ci;
            }
        }

        if (idx != c_idx[pi]) {
            unchanged = 0;
            c_idx[pi] = idx;
        }
    }
    return unchanged;
}

void update_centroids(float** points, int n_points, int n_dim, float** centroids, int K, int* c_idx)
{
    for (int ci = 0; ci < K; ++ci)
        for (int di = 0; di < n_dim; ++di)
            centroids[ci][di] = 0;

    // number of points in each cluster
    int* n_pts = (int*)malloc(K * sizeof(int));
    memset(n_pts, 0, K);

    int c = 0;
    for (int pi = 0; pi < n_points; ++pi) {
        c = c_idx[pi];
        n_pts[c]++;

        for (int di = 0; di < n_dim; ++di) {
            centroids[c][di] += points[pi][di];
        }
    }

    // average
    for (int ci = 0; ci < K; ++ci)
        for (int di = 0; di < n_dim; ++di)
            centroids[ci][di] /= n_pts[ci];

    free(n_pts);
}


void init_centroids(float** centroids, int K, float** points, int n_points, int n_dim)
{
    char* is_chosen = (char*)malloc(n_points * sizeof(char));
    memset(is_chosen, 0, n_points);

    srand(time(0));
    int choice;
    for (int ci = 0; ci < K; ++ci) {
        do {
            choice = rand() % n_points;
        } while (is_chosen[choice]);
        is_chosen[choice] = 1;

        // init the centroid with chosen point
        memcpy(centroids[ci], points[choice], n_dim * sizeof(float));
    }

    free(is_chosen);
}

float** kmeans(float** points, int n_points, int n_dim, int K, int max_iters, int* c_idx)
{
    // allocate space for centroids
    float** centroids = (float**)malloc(K * sizeof(float*));
    for (int ci = 0; ci < K; ++ci)
        centroids[ci] = (float*)malloc(n_dim * sizeof(float));

    memset(c_idx, 0, n_points);

    init_centroids(centroids, K, points, n_points, n_dim);
    printf("Init centroids completed.\n");

    int converge = 0, iters = 0;
    while (!converge && iters < max_iters) {
        converge = find_closest(points, n_points, n_dim, centroids, K, c_idx);
        update_centroids(points, n_points, n_dim, centroids, K, c_idx);
        ++iters;
    }

    if (!converge) {
        printf("Reaching maximum iterations, not converge yet.\n");
    }
    printf("clustering completed in %d iterations\n", iters);
    return centroids;
}

