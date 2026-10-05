package com.waterelixir.backend.dto;
import java.time.LocalDateTime;
public class ReadingDto {
    private Double waterLevel;
    private LocalDateTime recordedAt;
    
    public Double getWaterLevel() { return waterLevel; }
    public void setWaterLevel(Double waterLevel) { this.waterLevel = waterLevel; }
    public LocalDateTime getRecordedAt() { return recordedAt; }
    public void setRecordedAt(LocalDateTime recordedAt) { this.recordedAt = recordedAt; }
}
