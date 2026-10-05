package com.waterelixir.backend.model;
import jakarta.persistence.*;
@Entity
@Table(name="zone")
public class Zone {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="zone_id")
    private Long id;
    @Column(unique = true, nullable = false)
    private String name;
    @Column(name="zone_type")
    private String zoneType;
    @Column(name="valve_state")
    private String valveState = "OPEN";
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getZoneType() { return zoneType; }
    public void setZoneType(String zoneType) { this.zoneType = zoneType; }
    public String getValveState() { return valveState; }
    public void setValveState(String valveState) { this.valveState = valveState; }
}
