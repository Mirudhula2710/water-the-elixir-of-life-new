# Water Elixir - Spring Boot Backend (Phase 5)

This directory contains the modernized Java 17 backend for the Water Elixir project.

## Architecture
- **Language**: Java 17
- **Framework**: Spring Boot 3.4
- **Database**: MySQL (via Spring Data JPA)
- **Security**: Spring Security (HTTP Basic with BCrypt, stateless REST, CSRF disabled)

## Modules & Entities
- **Entities**: `Zone`, `Reading`, `Alert`, `Ticket`, `Complaint` mapped exactly to the 3NF MySQL schema.
- **DTOs**: Data Transfer Objects isolate the database schema from the API response shape.
- **AlertEvent OOP Hierarchy**: A custom abstract factory pattern handles severity prioritization instead of complex `if/else` ladders or messy database inheritance (D11/Phase 5).
- **Exceptions**: A `@RestControllerAdvice` guarantees clean, predictable JSON error payloads instead of ugly stack traces.

## Running Tests
No database is required for unit tests. They use MockMvc and Mockito.
```bash
./mvnw clean verify
```

## Running the App
Requires the `DB_PASSWORD` and `STAFF_PASSWORD` variables to be set in your terminal:
```bash
./mvnw spring-boot:run
```
