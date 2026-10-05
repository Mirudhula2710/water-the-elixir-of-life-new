package com.waterelixir.backend.model;
public class MediumAlertEvent extends AlertEvent {
    public MediumAlertEvent(Alert alert) { super(alert); }
    @Override public int priorityScore() { return 2; }
    @Override public String recommendedAction() { return "Monitor zone during next reading cycle."; }
}
