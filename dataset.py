"""Seed training data: typical Java comments labelled by intent."""
DATA = {
 "TODO": [
  "TODO: handle null input here", "TODO implement retry logic", "FIXME later, this is a temporary hack",
  "@todo add validation for the email field", "TODO: refactor this method into smaller pieces",
  "Need to add unit tests for this class", "TODO write better error messages", "Still to be done: support pagination",
  "XXX revisit this once the API is stable", "TODO: remove after migration is complete"],
 "BUG_FIX": [
  "Fix for issue #123: NPE when list is empty", "Bug fix: off-by-one error in loop index", "Workaround for bug in JDK 8 HashMap",
  "Fixed race condition when two threads update the cache", "Patch: prevent crash on malformed input", "Resolved memory leak by closing the stream",
  "Hotfix for wrong date format in production", "This was broken before, now handles empty strings correctly", "Fixes deadlock reported in ticket 4521",
  "Corrected wrong calculation of the total price"],
 "DOCUMENTATION": [
  "@param name the name of the user", "@return the number of elements in this list", "@throws IOException if the file cannot be read",
  "Returns the value associated with the given key", "Creates a new instance of the service with the given configuration",
  "@author John Smith", "Represents a customer order in the system", "@since 1.2 This class provides utility methods for string handling",
  "Gets the user identifier", "@see java.util.List for related collections",
  "Returns the total price of the order", "Returns true if the list contains the element", "Returns the name of this object",
  "Sets the value of the timeout property", "Returns a string representation of the object"],
 "EXPLANATION": [
  "loop through all items and sum the prices", "we use a stack here because order must be reversed", "skip the header row of the file",
  "check if the user is already logged in", "sort the list so binary search works later", "this is needed because the server returns null sometimes",
  "increment counter after each successful request", "initialize the buffer with default size", "compare both values to find the maximum",
  "first we open the connection then we send the query"],
 "COMMENTED_CODE": [
  "int x = 0;", "System.out.println(\"debug\" + value);", "if (user != null) { return user.getName(); }",
  "list.add(new Item(id, name));", "for (int i = 0; i < n; i++) {", "return result;", "String s = obj.toString();",
  "catch (Exception e) { e.printStackTrace(); }", "this.name = name;", "setVisible(true);"],
 "LICENSE": [
  "Copyright (c) 2015 Acme Corporation. All rights reserved.", "Licensed under the Apache License, Version 2.0",
  "This program is free software; you can redistribute it under the terms of the GNU General Public License",
  "Permission is hereby granted, free of charge, to any person obtaining a copy of this software",
  "Unless required by applicable law or agreed to in writing, software distributed under the License is provided as is",
  "MIT License copyright notice must be included in all copies", "All rights reserved. Unauthorized copying is prohibited",
  "See the LICENSE file for warranty and licensing details", "Copyright 2020 The Authors. Use of this source code is governed by a BSD license",
  "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied"],
}
