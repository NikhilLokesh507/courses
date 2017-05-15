#ifndef KMEANS_H
#define KMEANS_H

float** kmeans(float** points, int n_points, int n_dim, int K, int max_iters, int* c_idx);
int find_closest(float** points, int n_points, int n_dim, float** centroids, int K, int* c_idx);
void update_centroids(float** points, int n_points, int n_dim, float** centroids, int K, int* c_idx);
void init_centroids(float** centroids, int K, float** points, int n_points, int n_dim);
float avg_dist(float** points, int n_points, int n_dim, float** centroids, int K, int* c_idx);
#endif
