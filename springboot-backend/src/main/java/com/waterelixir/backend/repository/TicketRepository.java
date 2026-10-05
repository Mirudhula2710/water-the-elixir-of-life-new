package com.waterelixir.backend.repository;
import com.waterelixir.backend.model.Ticket;
import org.springframework.data.jpa.repository.JpaRepository;
public interface TicketRepository extends JpaRepository<Ticket, Long> {
    Ticket findByAlertId(Long alertId);
}
