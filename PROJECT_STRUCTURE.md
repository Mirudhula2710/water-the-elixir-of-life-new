# Project Structure: Water - The Elixir of Life

This document provides a detailed breakdown of every folder and critical file in the repository to help you understand the full-stack architecture of the project.

---

## 📁 Root Directory (Python Core & Flask)
The root directory holds the main orchestration scripts and the Flask web application.

- **`run_all.py`**: The master execution script. It uses `subprocess` to spin up the Flask dashboard, the AI Central Server, the Sensor Clients, and (optionally) the Spring Boot & Angular servers all in a single terminal window.
- **`app.py`**: The Flask web server. Handles routing, Jinja2 template rendering, dashboard logic, and dynamically switches between SQLite and MySQL based on environment variables. *Contains advanced assignment routing (`/auto_assign`, `/auto_assign_complaint`) for intelligent task distribution.*
- **`auth.py`**: Contains security decorators (e.g., `@login_required`, `@role_required`) to protect Flask routes.
- **`models.py`**: SQLAlchemy database schemas (`Zone`, `Reading`, `Alert`, `Ticket`, `Complaint`, `User`).
- **`severity_map.py`**: A shared utility that translates string-based physics severities (e.g., "Suspected Leak") into standard Database Enums (e.g., "HIGH").
- **`seed_users.py`** & **`import_sqlite_once.py`**: Utility scripts for generating default users (`users.db`) and migrating local SQLite telemetry data to the production MySQL database.
- **`requirements.txt`**: List of all Python dependencies (Flask, SQLAlchemy, Scikit-Learn, SymPy, Google Generative AI).

---

## 📁 `sensors/` (Telemetry & Processing Engine)
Handles real-time data generation and ingestion.

- **`zone_client.py`**: A socket client that simulates water tank physics using Torricelli's Law. It sends water level readings over TCP. It accepts a `--scenario` flag (normal, warning, critical) to simulate different leak severities.
- **`central_server.py`**: A robust, multiprocessing TCP server. It spawns an independent worker process for each campus zone. It receives data from the clients, evaluates it against the AI/Physics models, creates database alerts, and can trigger simulated "Valve Shutoffs".

---

## 📁 `detection/` (AI & Physics Evaluation)
The brain of the anomaly detection system.

- **`physics_model.py`**: Uses `SymPy` (symbolic mathematics) to evaluate Torricelli's formula and calculate the exact expected water level. 
- **`ml_model.py`**: Loads the trained Scikit-Learn model to evaluate the deviation and predict severity. Contains a safe fallback mechanism if the model file is missing.
- **`train_model.py`**: Generates a synthetic dataset based on physics thresholds and trains the Support Vector Machine (SVM_RBF) classification model.
- **`model_artifacts/`**: 
  - `severity_model.pkl`: The compiled Scikit-Learn AI model.
  - `feature_scaler.pkl` & `label_encoder.pkl`: Preprocessing utilities for the AI pipeline.
  - `model_metadata.json`: Stores the training metrics (Accuracy: 98.50%, F1 Score: 0.93).

---

## 📁 `gemini/` (LLM Integration)
- **`explain.py`**: Connects to the Google Gemini API. It takes raw telemetry metrics (e.g., "Deviation of -12.4 liters") and generates a human-readable, non-technical explanation and recommended action for the maintenance staff.

---

## 📁 `templates/` (Flask UI)
The HTML views for the Python web dashboard, utilizing Tailwind CSS for styling and Jinja2 for dynamic rendering.
- **`base.html`**: The master layout containing the navigation bar and CSS imports.
- **`manager.html`**: The 3-column tabbed dashboard for Managers. Includes advanced UI logic for auto-assigning system alerts and student complaints directly to workers.
- **`worker.html`**: A Kanban-style grid for maintenance workers to update ticket statuses and add resolution notes.
- **`student.html`**: A split-view page for students to submit complaints and track their lifecycle across three resolution phases.
- **`login.html`**: The authentication page.

---

## 📁 `springboot-backend/` (Java REST API)
A modern Java 17 backend providing a headless REST API for the telemetry data.

- **`src/main/java/com/waterelixir/backend/`**:
  - **`model/`**: JPA Entity classes representing the database tables. Includes the polymorphic `AlertEvent` abstract factory pattern to determine priority scores without database inheritance.
  - **`dto/`**: Data Transfer Objects to format JSON responses cleanly for the frontend.
  - **`repository/`**: Spring Data JPA interfaces for seamless database querying.
  - **`service/`**: `WaterService.java` contains the core business logic, transaction management, and ticket resolution logic.
  - **`controller/`**: REST controllers exposing endpoints (e.g., `/api/alerts`, `/api/tickets`).
  - **`security/`**: `SecurityConfig.java` implements stateless HTTP Basic authentication and CORS policies.
  - **`exception/`**: Global exception handler (`@RestControllerAdvice`) for returning clean JSON errors instead of stack traces.
- **`sql/`**: Contains `create_user.sql`, `schema.sql` (3NF mapped), and `seed.sql` for setting up the MySQL database.
- **`pom.xml`**: Maven configuration detailing Java dependencies.

---

## 📁 `angular-frontend/` (Modern Web App)
The independent Single Page Application (SPA) built with Angular 18.

- **`src/app/`**:
  - **`models/models.ts`**: TypeScript interfaces that perfectly mirror the Java DTOs.
  - **`services/`**: Contains `api.service.ts` (HttpClient requests to Spring Boot) and `auth.interceptor.ts` (automatically injects the Basic Auth headers into outgoing requests).
- **`angular.json` & `package.json`**: Build configuration and NPM dependency lists.

---

## 📁 `data/`
- **`water_leak_sensor_dataset.csv`**: The synthetic training data generated by `train_model.py` used to teach the AI how to identify campus water leaks.
