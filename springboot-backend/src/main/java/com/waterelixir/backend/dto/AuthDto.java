package com.waterelixir.backend.dto;
public class AuthDto {
    private String username;
    private String role;
    
    public AuthDto(String username, String role) {
        this.username = username;
        this.role = role;
    }
    public String getUsername() { return username; }
    public String getRole() { return role; }
}
