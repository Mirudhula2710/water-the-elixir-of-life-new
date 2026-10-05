package com.waterelixir.backend.model;
public class CriticalAlertEvent extends AlertEvent {
    public CriticalAlertEvent(Alert alert) { super(alert); }
    @Override public int priorityScore() { return 4; }
    @Override public String recommendedAction() { return "Immediate action required! Valve has been shut off."; }
}
