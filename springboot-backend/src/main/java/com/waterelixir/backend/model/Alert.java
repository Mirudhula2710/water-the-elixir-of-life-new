package com.waterelixir.backend.model;
import jakarta.persistence.*;
import java.time.LocalDateTime;
@Entity
@Table(name="alert")
public class Alert {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="alert_id")
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="zone_id", nullable=false)
    private Zone zone;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="reading_id")
    private Reading reading;
    @Enumerated(EnumType.STRING)
    @Column(nullable=false)
    private Severity severity;
    @Column(name="expected_level")
    private Double expectedLevel;
    private Double deviation;
    private String message;
    @Column(name="gemini_explanation")
    private String geminiExplanation;
    private String status = "OPEN";
    @Column(name="created_at", nullable=false)
    private LocalDateTime createdAt;
    @Column(name="resolved_at")
    private LocalDateTime resolvedAt;
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Zone getZone() { return zone; }
    public void setZone(Zone zone) { this.zone = zone; }
    public Reading getReading() { return reading; }
    public void setReading(Reading reading) { this.reading = reading; }
    public Severity getSeverity() { return severity; }
    public void setSeverity(Severity severity) { this.severity = severity; }
    public Double getExpectedLevel() { return expectedLevel; }
    public void setExpectedLevel(Double expectedLevel) { this.expectedLevel = expectedLevel; }
    public Double getDeviation() { return deviation; }
    public void setDeviation(Double deviation) { this.deviation = deviation; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public String getGeminiExplanation() { return geminiExplanation; }
    public void setGeminiExplanation(String geminiExplanation) { this.geminiExplanation = geminiExplanation; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getResolvedAt() { return resolvedAt; }
    public void setResolvedAt(LocalDateTime resolvedAt) { this.resolvedAt = resolvedAt; }
}
