package com.waterelixir.backend.model;
import jakarta.persistence.*;
import java.time.LocalDateTime;
@Entity
@Table(name="ticket")
public class Ticket {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="ticket_id")
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="alert_id", nullable=false)
    private Alert alert;
    private String status = "OPEN";
    private String notes;
    @Column(name="created_at", nullable=false)
    private LocalDateTime createdAt;
    @Column(name="resolved_at")
    private LocalDateTime resolvedAt;
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Alert getAlert() { return alert; }
    public void setAlert(Alert alert) { this.alert = alert; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public LocalDateTime getResolvedAt() { return resolvedAt; }
    public void setResolvedAt(LocalDateTime resolvedAt) { this.resolvedAt = resolvedAt; }
}
