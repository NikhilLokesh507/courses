
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;

public class PercolationStats {
    private double[] result;
    private int gridSize;
    private int trialTimes;


    public PercolationStats(int n, int trials) {
        if (n <= 0 || trials <= 0)
            throw new IllegalArgumentException();
        gridSize = n;
        result = new double[trials];
        trialTimes = trials;
        int i, j, count = 0;
        for (int t = 0; t < trialTimes; t++) {
            Percolation perc = new Percolation(gridSize);
            count = 0;
            while (!perc.percolates()) {
                i = StdRandom.uniform(gridSize);
                j = StdRandom.uniform(gridSize);
                i++;
                j++;
                if (!perc.isOpen(i, j)) {
                    perc.open(i, j);
                    count++;
                }
            }
            result[t] = (double) count / (gridSize*gridSize);
        }
    }

    public double mean() {
        return StdStats.mean(result);
    }

    public double stddev() {
        return StdStats.stddev(result);
    }

    public double confidenceLo() {
        return mean() - 1.96 * stddev() / Math.sqrt(trialTimes);
    }

    public double confidenceHi() {
        return mean() + 1.96 * stddev() / Math.sqrt(trialTimes);
    }

    public static void main(String[] args) {
        int n = 0, trials = 0;
        if (args.length != 2) {
            throw new IllegalArgumentException("2 parameters required");
        }
        n = Integer.parseInt(args[0]);
        trials = Integer.parseInt(args[1]);
        PercolationStats stats = new PercolationStats(n, trials);
        
        StdOut.printf("mean \t = %f\n", stats.mean());
        StdOut.printf("stddev \t = %f\n", stats.stddev());
        StdOut.printf("95%% confidence interval \t = %f, %f\n", stats.confidenceLo(), stats.confidenceHi());

    }
}
