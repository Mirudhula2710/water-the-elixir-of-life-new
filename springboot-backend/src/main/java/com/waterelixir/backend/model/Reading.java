package com.waterelixir.backend.model;
import jakarta.persistence.*;
import java.time.LocalDateTime;
@Entity
@Table(name="reading")
public class Reading {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="reading_id")
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="zone_id", nullable=false)
    private Zone zone;
    @Column(name="water_level", nullable=false)
    private Double waterLevel;
    @Column(name="flow_rate")
    private Double flowRate;
    @Column(name="recorded_at", nullable=false)
    private LocalDateTime recordedAt;
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Zone getZone() { return zone; }
    public void setZone(Zone zone) { this.zone = zone; }
    public Double getWaterLevel() { return waterLevel; }
    public void setWaterLevel(Double waterLevel) { this.waterLevel = waterLevel; }
    public Double getFlowRate() { return flowRate; }
    public void setFlowRate(Double flowRate) { this.flowRate = flowRate; }
    public LocalDateTime getRecordedAt() { return recordedAt; }
    public void setRecordedAt(LocalDateTime recordedAt) { this.recordedAt = recordedAt; }
}
