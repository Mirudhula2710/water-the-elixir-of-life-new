package com.waterelixir.backend.model;
public class LowAlertEvent extends AlertEvent {
    public LowAlertEvent(Alert alert) { super(alert); }
    @Override public int priorityScore() { return 1; }
    @Override public String recommendedAction() { return "No action needed."; }
}
