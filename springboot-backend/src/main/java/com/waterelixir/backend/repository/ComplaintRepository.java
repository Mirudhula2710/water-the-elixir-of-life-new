package com.waterelixir.backend.repository;
import com.waterelixir.backend.model.Complaint;
import org.springframework.data.jpa.repository.JpaRepository;
public interface ComplaintRepository extends JpaRepository<Complaint, Long> {}
