package com.waterelixir.backend.model;
public class HighAlertEvent extends AlertEvent {
    public HighAlertEvent(Alert alert) { super(alert); }
    @Override public int priorityScore() { return 3; }
    @Override public String recommendedAction() { return "Dispatch maintenance to check for minor leaks."; }
}
