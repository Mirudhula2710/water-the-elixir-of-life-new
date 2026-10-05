package com.waterelixir.backend.repository;
import com.waterelixir.backend.model.Reading;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import org.springframework.data.domain.Pageable;
public interface ReadingRepository extends JpaRepository<Reading, Long> {
    List<Reading> findByZoneIdOrderByRecordedAtDesc(Long zoneId, Pageable pageable);
}
