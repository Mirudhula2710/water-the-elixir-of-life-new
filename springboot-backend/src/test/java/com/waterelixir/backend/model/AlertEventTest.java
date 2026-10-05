package com.waterelixir.backend.model;
import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

public class AlertEventTest {
    @Test
    public void testPolymorphismAndSorting() {
        Alert a1 = new Alert(); a1.setSeverity(Severity.LOW);
        Alert a2 = new Alert(); a2.setSeverity(Severity.CRITICAL);
        Alert a3 = new Alert(); a3.setSeverity(Severity.MEDIUM);
        
        AlertEvent e1 = AlertEventFactory.createEvent(a1);
        AlertEvent e2 = AlertEventFactory.createEvent(a2);
        
        assertTrue(e1 instanceof LowAlertEvent);
        assertTrue(e2 instanceof CriticalAlertEvent);
        assertEquals(1, e1.priorityScore());
        assertEquals(4, e2.priorityScore());
        
        List<Alert> alerts = Arrays.asList(a1, a2, a3);
        alerts.sort(Comparator.comparing((Alert a) -> a.getSeverity().priority()).reversed());
        
        assertEquals(Severity.CRITICAL, alerts.get(0).getSeverity());
        assertEquals(Severity.MEDIUM, alerts.get(1).getSeverity());
        assertEquals(Severity.LOW, alerts.get(2).getSeverity());
    }
}
