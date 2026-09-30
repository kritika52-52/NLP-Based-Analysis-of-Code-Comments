/*
 * Copyright (c) 2020 Acme Corp. Licensed under the Apache License, Version 2.0
 */
package demo;

/**
 * Represents a customer order.
 * @author Jane
 */
public class Sample {
    /** Returns the total price of the order. */
    public double total(java.util.List<Double> prices) {
        double sum = 0; // loop through all items and sum the prices
        for (double p : prices) sum += p;
        // TODO: handle discounts
        // Fix for issue #42: NPE when list is empty
        // System.out.println("total=" + sum);
        return sum;
    }
}
