package com.waterelixir.backend.dto;
public class ZoneDto {
    private Long id;
    private String name;
    private String valveState;
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getValveState() { return valveState; }
    public void setValveState(String valveState) { this.valveState = valveState; }
}
