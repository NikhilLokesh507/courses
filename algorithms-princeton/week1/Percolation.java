
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class Percolation {
    private WeightedQuickUnionUF unionUF;
    private WeightedQuickUnionUF unionUFForFull;
    private int gridSize;
    private boolean[] status;
    private int virtualTop;
    private int virtualBottom;

    public Percolation(int n) {
        if (n <= 0)
            throw new IllegalArgumentException();
        unionUF = new WeightedQuickUnionUF(n*n+2);
        unionUFForFull = new WeightedQuickUnionUF(n*n+1);
        gridSize = n;
        virtualTop = n*n;
        virtualBottom = n*n+1;

        status = new boolean[n*n];
    }
    private int index(int i, int j) {
        if (i < 1 || i > gridSize || j < 1 || j > gridSize) {
            throw new IndexOutOfBoundsException();
        }
        return (i-1)*gridSize + j - 1;
    }
    private void union(int i1, int j1, int i2, int j2) {
        unionUF.union(index(i1, j1), index(i2, j2));
        unionUFForFull.union(index(i1, j1), index(i2, j2));
    }

    private void union(int i1, int j1, int virtual) {
        unionUF.union(index(i1, j1), virtual);
        if (virtual == virtualTop)
            unionUFForFull.union(index(i1, j1), virtual);
    }
    public void open(int i, int j) {
        if (isOpen(i, j))
            return;
        status[index(i, j)] = true;
        if (i > 1 && isOpen(i-1, j))
            union(i-1, j, i, j);
        if (i < gridSize && isOpen(i+1, j))
            union(i+1, j, i, j);
        if (j > 1 && isOpen(i, j-1))
            union(i, j-1, i, j);
        if (j < gridSize && isOpen(i, j+1))
            union(i, j+1, i, j);
        if (i == 1)
            union(i, j, virtualTop);
        if (i == gridSize)
            union(i, j, virtualBottom);
    }

    public boolean isOpen(int i, int j) {
        return status[index(i, j)];
    }

    public boolean isFull(int i, int j) {
        return unionUFForFull.connected(index(i, j), virtualTop);
    }

    public boolean percolates() {
        return unionUF.connected(virtualTop, virtualBottom);
    }

    public static void main(String[] args) {
        Percolation perc = new Percolation(100);
        StdOut.println(perc.isOpen(100, 100));
        perc.open(1, 1);
        StdOut.println(perc.isOpen(1, 1));
        StdOut.println(perc.percolates());

        perc.open(2, 2);

        StdOut.println(perc.percolates());
    }
}
