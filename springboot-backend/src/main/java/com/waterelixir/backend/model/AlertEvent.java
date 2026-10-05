package com.waterelixir.backend.model;
public abstract class AlertEvent {
    protected Alert alert;
    public AlertEvent(Alert alert) { this.alert = alert; }
    public abstract int priorityScore();
    public abstract String recommendedAction();
}
