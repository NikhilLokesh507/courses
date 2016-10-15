/**
 * Created by kevin on 14/10/2016.
 */

import edu.princeton.cs.algs4.StdOut;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class Deque<Item> implements Iterable<Item> {

    private Node first = null;
    private Node last = null;
    private int size = 0;

    private class Node
    {
        Item item;
        Node prev;
        Node next;
    }

    public Deque() {
        first = new Node();
        last = new Node();
        first.next = last;
        last.prev = first;
        size = 0;
    }

    public boolean isEmpty() {
        return first.next == last;
    }

    public int size() {
        return size;
    }

    public void addFirst(Item item) {
        if (item == null) {
            throw new NullPointerException();
        }
        Node front = new Node();
        Node next = first.next;

        front.item = item;
        front.prev = first;
        front.next = next;

        first.next = front;
        next.prev = front;
        ++size;
    }

    public void addLast(Item item) {
        if (item == null) {
            throw new NullPointerException();
        }
        Node back = new Node();
        Node prev = last.prev;

        back.item = item;
        back.next = last;
        back.prev = prev;

        last.prev = back;
        prev.next = back;
        ++size;
    }

    public Item removeFirst() {
        if (size <= 0) {
            throw new NoSuchElementException();
        }
        Node front = first.next;
        Item item = front.item;

        Node newFront = front.next;
        first.next = newFront;
        newFront.prev = first;
        --size;
        return item;
    }

    public Item removeLast() {
        if (size <= 0) {
            throw new NoSuchElementException();
        }
        Node back = last.prev;
        Item item = back.item;

        Node newBack = back.prev;
        last.prev = newBack;
        newBack.next = last;
        --size;
        return item;
    }

    public Iterator<Item> iterator() {
        return new DequeIterator();
    }

    private class DequeIterator implements Iterator<Item>
    {
        private Node current = first.next;

        public boolean hasNext() { return current != last; }
        public void remove()     { throw new UnsupportedOperationException(); }
        public Item next()
        {
            if (current.item == null) {
                throw new NoSuchElementException();
            }
            Item item = current.item;
            current = current.next;
            return item;
        }
    }

    public static void main(String[] args) {
        Deque<String> test = new Deque<String>();
        test.addFirst("front1");
        test.addFirst("front0");
        test.addLast("back1");
        test.addLast("back0");

        Iterator<String> i = test.iterator();
        while (i.hasNext())
        {
            String s = i.next();
            StdOut.println(s);
        }

        test.removeFirst();
        test.removeLast();
        i = test.iterator();
        while (i.hasNext())
        {
            String s = i.next();
            StdOut.println(s);
        }

        test.removeFirst();
        i = test.iterator();
        while (i.hasNext())
        {
            String s = i.next();
            StdOut.println(s);
        }

        test.removeLast();
        i = test.iterator();
        while (i.hasNext())
        {
            String s = i.next();
            StdOut.println(s);
        }

        // empty deque
        test.removeFirst();
    }
}
