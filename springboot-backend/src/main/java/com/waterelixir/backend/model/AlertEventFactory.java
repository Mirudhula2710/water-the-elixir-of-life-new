package com.waterelixir.backend.model;
public class AlertEventFactory {
    public static AlertEvent createEvent(Alert alert) {
        if (alert.getSeverity() == null) return new LowAlertEvent(alert);
        switch (alert.getSeverity()) {
            case MEDIUM: return new MediumAlertEvent(alert);
            case HIGH: return new HighAlertEvent(alert);
            case CRITICAL: return new CriticalAlertEvent(alert);
            case LOW:
            default: return new LowAlertEvent(alert);
        }
    }
}
