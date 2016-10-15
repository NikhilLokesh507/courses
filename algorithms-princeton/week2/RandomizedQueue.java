import java.util.Iterator;
import java.util.NoSuchElementException;

import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.StdRandom;

/**
 * Created by kevin on 14/10/2016.
 */
public class RandomizedQueue<Item> implements Iterable<Item> {
    private Item[] items;
    private int size = 0;
    private int capacity = 2;

    public RandomizedQueue() {
        items = (Item[]) new Object[capacity];
        size = 0;
    }

    private void resize(int newCapacity)
    {
        Item[] copy = (Item[]) new Object[newCapacity];
        for (int i = 0; i < size; ++i) {
            copy[i] = items[i];
        }
        items = copy;
        capacity = newCapacity;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public int size() {
        return size;
    }

    public void enqueue(Item item) {
        if (item == null) {
            throw new NullPointerException();
        }
        if (size == capacity) {
            resize(capacity * 2);
        }
        items[size++] = item;
    }

    public Item dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException();
        }
        int index = StdRandom.uniform(size);
        Item item = items[index];
        items[index] = items[--size];
        items[size] = null;
        if (size > 0 && size == capacity / 4) resize(capacity/2);
        return item;
    }

    public Item sample() {
        if (isEmpty()) {
            throw new NoSuchElementException();
        }
        int index = StdRandom.uniform(size);
        Item item = items[index];
        return item;
    }

    public Iterator<Item> iterator() {
        return new RandomizedQueueIterator();
    }
    private class RandomizedQueueIterator implements Iterator<Item> {
        private int[] accessArray;
        private int current;

        public RandomizedQueueIterator() {
            accessArray = new int[size];
            for (int i = 0; i < size; ++i) {
                accessArray[i] = i;
            }
            StdRandom.shuffle(accessArray);
            current = 0;
        }

        public boolean hasNext() { return current != accessArray.length; }
        public void remove()     { throw new UnsupportedOperationException(); }
        public Item next()
        {
            if (current >= accessArray.length) {
                throw new NoSuchElementException();
            }
            int index = accessArray[current];
            Item item = items[index];
            current++;
            return item;
        }
    }

    public static void main(String[] args) {
        RandomizedQueue<Integer> rq = new RandomizedQueue<>();
//        rq.size();
//        rq.isEmpty();
//        rq.enqueue(32);
//        rq.dequeue();
//        rq.enqueue(5);
//        rq.dequeue();
//        rq.enqueue(22);
        Iterator<Integer> ii = rq.iterator();
        ii.next();
    }

}
