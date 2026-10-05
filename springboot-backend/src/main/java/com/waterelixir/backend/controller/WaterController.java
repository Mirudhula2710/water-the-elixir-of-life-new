package com.waterelixir.backend.controller;

import com.waterelixir.backend.dto.*;
import com.waterelixir.backend.service.WaterService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/api")
public class WaterController {

    @Autowired
    private WaterService waterService;

    @GetMapping("/zones")
    public List<ZoneDto> getZones() {
        return waterService.getZones();
    }

    @GetMapping("/alerts")
    public List<AlertDto> getAlerts(@RequestParam(required = false) String severity,
                                    @RequestParam(required = false) Long zoneId) {
        return waterService.getAlerts(severity, zoneId);
    }

    @GetMapping("/zones/{zoneId}/readings")
    public List<ReadingDto> getReadings(@PathVariable Long zoneId,
                                        @RequestParam(defaultValue = "50") int limit) {
        return waterService.getReadings(zoneId, limit);
    }

    @PostMapping("/complaints")
    public ResponseEntity<?> createComplaint(@Valid @RequestBody ComplaintDto dto) {
        Long id = waterService.createComplaint(dto);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest()
                .path("/{id}").buildAndExpand(id).toUri();
        return ResponseEntity.created(location).build();
    }

    @PutMapping("/tickets/{ticketId}")
    public ResponseEntity<?> updateTicket(@PathVariable Long ticketId,
                                          @Valid @RequestBody TicketUpdateDto dto) {
        waterService.updateTicket(ticketId, dto);
        return ResponseEntity.ok().build();
    }

    @DeleteMapping("/alerts/{alertId}")
    public ResponseEntity<?> deleteAlert(@PathVariable Long alertId) {
        waterService.deleteAlert(alertId);
        return ResponseEntity.noContent().build();
    }
}
