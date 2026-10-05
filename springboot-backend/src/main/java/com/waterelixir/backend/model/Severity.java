package com.waterelixir.backend.model;
public enum Severity {
    LOW(1), MEDIUM(2), HIGH(3), CRITICAL(4);
    private final int priority;
    Severity(int priority) { this.priority = priority; }
    public int priority() { return priority; }
}
