package com.waterelixir.backend.model;
import jakarta.persistence.*;
import java.time.LocalDateTime;
@Entity
@Table(name="complaint")
public class Complaint {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="complaint_id")
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="zone_id", nullable=false)
    private Zone zone;
    @Column(nullable=false)
    private String description;
    private String category;
    private String priority;
    @Column(name="triage_note")
    private String triageNote;
    private String status = "NEW";
    @Column(name="created_at", nullable=false)
    private LocalDateTime createdAt;
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Zone getZone() { return zone; }
    public void setZone(Zone zone) { this.zone = zone; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getPriority() { return priority; }
    public void setPriority(String priority) { this.priority = priority; }
    public String getTriageNote() { return triageNote; }
    public void setTriageNote(String triageNote) { this.triageNote = triageNote; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
