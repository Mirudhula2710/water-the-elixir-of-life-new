package com.waterelixir.backend.repository;
import com.waterelixir.backend.model.Alert;
import com.waterelixir.backend.model.Severity;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
public interface AlertRepository extends JpaRepository<Alert, Long> {
    List<Alert> findBySeverityAndZoneId(Severity severity, Long zoneId);
    List<Alert> findBySeverity(Severity severity);
    List<Alert> findByZoneId(Long zoneId);
}
