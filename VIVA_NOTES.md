# VIVA NOTES

1. **What is Spring Data JPA?**
   It's a part of the larger Spring Data family that makes it easier to implement JPA-based repositories, greatly reducing boilerplate code.

2. **Why use @RestController?**
   It combines `@Controller` and `@ResponseBody`, meaning the returned object is automatically serialized into JSON and passed back into the HttpResponse object.

3. **What is the use of @Entity?**
   It marks the class as a JPA entity, meaning it maps to a table in the database.

4. **Why do we use DTOs instead of Entities?**
   DTOs (Data Transfer Objects) hide internal database structures, prevent over-posting vulnerabilities, and allow us to format the data exactly as the frontend needs it without coupling the API to the database schema.

5. **What does `spring.jpa.hibernate.ddl-auto=validate` do?**
   It tells Hibernate to validate the database schema against the entity mappings on startup, ensuring they match, but it will NOT modify or drop the tables. This is safe for production.

6. **What is 3NF (Third Normal Form)?**
   A database is in 3NF if it is in 2NF and all its columns are non-transitively dependent on the primary key. In our `alert` table, `severity`, `deviation`, and `expected_level` depend only on `alert_id`.

7. **Why is `zone_id` a foreign key in `alert`?**
   To strictly enforce referential integrity so that every alert belongs to exactly one existing zone.

8. **How does lazy loading (`FetchType.LAZY`) work?**
   It defers the initialization of an association until it is explicitly accessed, which improves performance by avoiding unnecessary database queries.

9. **Explain `EnumType.STRING` in JPA.**
   By default, enums are saved as integers (ordinals). Using `EnumType.STRING` saves the string name (e.g. "CRITICAL") to the database, which is readable and safe against enum reordering.

10. **What is HTTP Basic Authentication?**
    A simple authentication scheme built into the HTTP protocol where the client sends the username and password encoded in base64 in the `Authorization` header.

11. **Why do we use BCrypt for passwords?**
    BCrypt is a one-way hashing algorithm that automatically handles salting and is computationally intensive, making it highly resistant to brute-force and rainbow table attacks.

12. **Why is CSRF disabled in our Security Config?**
    CSRF (Cross-Site Request Forgery) protection is necessary for session/cookie-based apps. Since our API is stateless and uses HTTP Basic Auth (tokens passed in headers), CSRF is not required.

13. **What is CORS and how did you configure it?**
    Cross-Origin Resource Sharing allows a web application running at one origin (e.g. `localhost:4200`) to access resources from a different origin (e.g. `localhost:8080`). We configured it globally in `SecurityConfig`.

14. **Explain `@RestControllerAdvice`.**
    It allows us to handle exceptions across the whole application in one global component, intercepting exceptions and returning structured JSON error responses.

15. **What is polymorphism in our `AlertEvent` implementation?**
    `AlertEvent` is an abstract class with subclasses for each severity. Instead of using `switch` statements everywhere, we call `priorityScore()` and it dynamically executes the correct subclass's method (method overriding).

16. **Why did we avoid JPA Inheritance for `AlertEvent`?**
    We wanted plain OOP logic for our service layer without forcing JPA to map subclasses to database tables (like Single Table or Joined strategies), keeping the DB schema simple.

17. **What is a TreeSet and why use it for Alerts?**
    A `TreeSet` is a collection that automatically sorts its elements. We used it with a custom comparator to sort alerts by `priorityScore` first, and then by `createdAt` descending.

18. **Explain the Maven Lifecycle.**
    It is a sequence of phases (like `validate`, `compile`, `test`, `package`, `verify`, `install`, `deploy`) that defines the build process. Running `mvnw verify` runs all phases up to integration testing.

19. **What does `@Valid` do?**
    It triggers Bean Validation (Hibernate Validator) on the incoming request body, ensuring constraints like `@NotNull` or `@NotBlank` in the DTO are met before the controller method runs.

20. **Why use `@MockBean` in `@WebMvcTest`?**
    `@WebMvcTest` only loads the web layer (Controllers). We use `@MockBean` to inject a fake (mocked) `WaterService` so we can test the controller without a database or full application context.

21. **How do we handle 404s cleanly?**
    By throwing a custom `ResourceNotFoundException` annotated with `@ResponseStatus(HttpStatus.NOT_FOUND)`, which our `@RestControllerAdvice` catches and formats into a JSON error.

22. **What HTTP method is used for updating tickets and why?**
    `PUT` (or `PATCH`). `PUT` replaces the resource or updates its state. We use it for `/api/tickets/{ticketId}`.

23. **What does `ResponseEntity.created(location).build()` do?**
    It returns a 201 Created status code and sets the HTTP `Location` header pointing to the URI of the newly created resource, following REST best practices.

24. **Why is `app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` set in Flask?**
    It disables the modification tracker which uses significant memory and is usually unnecessary unless using Flask-SQLAlchemy's event system.

25. **How does the ML fallback work?**
    In `ml_model.py`, if the model fails to load, it explicitly logs a warning and returns `Normal`. The `central_server.py` then uses the physics severity (Torricelli's law output) as the fallback.
