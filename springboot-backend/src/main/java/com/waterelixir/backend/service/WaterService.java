package com.waterelixir.backend.service;

import com.waterelixir.backend.dto.*;
import com.waterelixir.backend.exception.InvalidRequestException;
import com.waterelixir.backend.exception.ResourceNotFoundException;
import com.waterelixir.backend.model.*;
import com.waterelixir.backend.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class WaterService {
    @Autowired private ZoneRepository zoneRepository;
    @Autowired private AlertRepository alertRepository;
    @Autowired private ReadingRepository readingRepository;
    @Autowired private ComplaintRepository complaintRepository;
    @Autowired private TicketRepository ticketRepository;

    public List<ZoneDto> getZones() {
        return zoneRepository.findAll().stream().map(z -> {
            ZoneDto dto = new ZoneDto();
            dto.setId(z.getId());
            dto.setName(z.getName());
            dto.setValveState(z.getValveState());
            return dto;
        }).collect(Collectors.toList());
    }

    public List<ReadingDto> getReadings(Long zoneId, int limit) {
        if (!zoneRepository.existsById(zoneId)) throw new ResourceNotFoundException("Zone not found");
        return readingRepository.findByZoneIdOrderByRecordedAtDesc(zoneId, PageRequest.of(0, limit))
                .stream().map(r -> {
                    ReadingDto dto = new ReadingDto();
                    dto.setWaterLevel(r.getWaterLevel());
                    dto.setRecordedAt(r.getRecordedAt());
                    return dto;
                }).collect(Collectors.toList());
    }

    public List<AlertDto> getAlerts(String severityStr, Long zoneId) {
        List<Alert> alerts;
        Severity sev = null;
        if (severityStr != null && !severityStr.isEmpty()) {
            try {
                sev = Severity.valueOf(severityStr.toUpperCase());
            } catch (IllegalArgumentException e) {
                throw new InvalidRequestException("Invalid severity. Allowed: LOW, MEDIUM, HIGH, CRITICAL");
            }
        }

        if (sev != null && zoneId != null) {
            alerts = alertRepository.findBySeverityAndZoneId(sev, zoneId);
        } else if (sev != null) {
            alerts = alertRepository.findBySeverity(sev);
        } else if (zoneId != null) {
            alerts = alertRepository.findByZoneId(zoneId);
        } else {
            alerts = alertRepository.findAll();
        }

        // Sort using TreeSet with custom comparator for severity order
        TreeSet<Alert> sortedAlerts = new TreeSet<>(Comparator.comparing((Alert a) -> a.getSeverity().priority()).reversed()
                .thenComparing(Alert::getCreatedAt).reversed());
        sortedAlerts.addAll(alerts);

        return sortedAlerts.stream().map(a -> {
            AlertDto dto = new AlertDto();
            dto.setId(a.getId());
            dto.setZoneName(a.getZone().getName());
            dto.setSeverity(a.getSeverity().name());
            dto.setGeminiExplanation(a.getGeminiExplanation());
            
            AlertEvent event = AlertEventFactory.createEvent(a);
            dto.setPriority(event.priorityScore());
            dto.setRecommendedAction(event.recommendedAction());
            
            Ticket t = ticketRepository.findByAlertId(a.getId());
            if (t != null) {
                dto.setTicketId(t.getId());
                dto.setTicketStatus(t.getStatus());
            }
            return dto;
        }).collect(Collectors.toList());
    }

    @Transactional
    public Long createComplaint(ComplaintDto dto) {
        Zone zone = zoneRepository.findById(dto.getZoneId())
                .orElseThrow(() -> new ResourceNotFoundException("Zone not found"));
        Complaint c = new Complaint();
        c.setZone(zone);
        c.setDescription(dto.getDescription());
        c.setCategory(dto.getCategory());
        c.setPriority(dto.getPriority());
        c.setCreatedAt(LocalDateTime.now());
        return complaintRepository.save(c).getId();
    }

    @Transactional
    public void updateTicket(Long ticketId, TicketUpdateDto dto) {
        Ticket t = ticketRepository.findById(ticketId)
                .orElseThrow(() -> new ResourceNotFoundException("Ticket not found"));
        
        String newStatus = dto.getStatus().toUpperCase();
        if (!Arrays.asList("OPEN", "IN_PROGRESS", "RESOLVED").contains(newStatus)) {
            throw new InvalidRequestException("Invalid status");
        }
        
        t.setStatus(newStatus);
        if (dto.getNotes() != null) t.setNotes(dto.getNotes());
        
        if ("RESOLVED".equals(newStatus)) {
            t.setResolvedAt(LocalDateTime.now());
            if (t.getAlert() != null) {
                t.getAlert().setStatus("RESOLVED");
                Zone z = t.getAlert().getZone();
                if (z != null) z.setValveState("OPEN");
            }
        }
    }

    @Transactional
    public void deleteAlert(Long alertId) {
        if (!alertRepository.existsById(alertId)) throw new ResourceNotFoundException("Alert not found");
        alertRepository.deleteById(alertId);
    }
}
