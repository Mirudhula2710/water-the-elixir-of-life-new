# Phase 0 - Baseline and Checkpoint Report

## 1. Backup, Checksums, and Repo Map
- **Backup Created**: A full backup was created outside the repository at `../water_backup_<timestamp>`.
- **Git Branch**: Created local branch `finish-all-modules` to track progress.
- **Repository Mapping**: The project resides at `c:\python310\water-the-elixir-of-life-main (1)\water-the-elixir-of-life-main`. There is a second copy at `c:\python310\water-the-elixir-of-life-main`. A read-only comparison confirms all `.py` files are identical between the two copies.
- **Data Validation**: Confirmed that `data/water_leak_sensor_dataset.csv` exists. Re-measured threshold bands directly from the dataset.

## 2. Tools & Environment Check
- **Installed Tools**:
  - `java` (Found: JDK 21. Configured Maven to use `maven.compiler.release=17`).
  - `node` (Found)
  - `python` (Found)
  - `pip` (Found)
  - `mysql` (Not found in PATH; the DB and user will be manually created by the user).
- **Housekeeping**: Scratch files were moved to `../audit_scratch` and `venv/` was added to `.gitignore`.

## 3. Re-Verification of Current State
- **M1 (~80%)**: 
  - `sensors/zone_client.py` uses `multiprocessing.Process` but does NOT accept `--scenario` or `--zone` arguments (currently hardcoded zones in a loop). 
  - `sensors/central_server.py` uses TCP port 65432, but currently uses `threading.Thread` instead of multiprocessing. It does not set `SO_REUSEADDR`.
- **M2 (~50%)**: 
  - `detection/physics_model.py` exists and uses SymPy. 
  - `detection/ml_model.py` and `severity_model.pkl` exist, but the model fails to load with error `_pickle.UnpicklingError: STACK_GLOBAL requires str` due to an `InconsistentVersionWarning` (trained on scikit-learn 1.6.1, loading on 1.9.1).
  - No training script exists. `model_metadata.json` metrics are **unverifiable**.
- **M3 (~50%)**: 
  - `gemini/explain.py`, `app.py` (Flask dashboard), and SQLite models exist.
  - **D12 Application**: The Flask app (`app.py`) has roles (manager, worker, student). Per D12, these roles and login behaviors will be kept intact in a small separate SQLite file used ONLY for Flask authentication.
- **M4, M5**: Not yet built.

## 4. Open Item Resolutions
**O2: Maintenance tickets and simulated valve shutoff**
- **Fact**: They exist and operate as expected. Running a simulated TC04 (Critical leak: Level -50.0) yields the following server log:
  ```
  [Hostel Blocks] Level: -50.00 (Expected: 0.00) -> Severity: Critical
  *** CRITICAL ALERT in Hostel Blocks *** Simulated Valve Shutoff executed.
  ```
- **Migration**: As requested, these will be migrated to the new MySQL/Spring/Angular architecture exactly as they are.

## 5. Threshold Bands (Derived from Data)
Based on the dataset and the directive to treat gaps as `Normal`:
- **Critical**: `<= -20.0` OR `>= 28.0`
- **Suspected Leak**: `< -10.0` (and `> -20.0`)
- **Warning**: `< -4.25` (and `>= -10.0`)
- **Normal**: Any other value.

## 6. Defaults to Apply
- **F2**: Existing SQLite data will be imported ONCE into MySQL (read-only, idempotent).
- **F3**: Angular will use plain hand-written CSS.
- **F4**: Gemini will use the `GEMINI_API_KEY` with a request timeout and a clear template fallback text on failure.

## 7. Ambiguities & Clarifications
1. **Flask Database Splitting (D12)**: The Flask login users and roles will stay in a separate SQLite database. All sensor data, readings, alerts, tickets, complaints, and zones will go to MySQL. This will be achieved using Flask-SQLAlchemy binds (e.g., `SQLALCHEMY_BINDS = {'users': 'sqlite:///users.db'}`) or equivalent session handling.
2. **Dataset Creation**: The synthetic dataset was generated with a custom Python script. This will be documented in the README and model metadata.
3. **Baseline TC01-TC04**: Explicit `--scenario` arguments are not yet supported, so TC01-TC04 cannot be explicitly run. However, the random baseline injection produces the required critical logs (as proven above).

---
**Status**: Phase 0 Complete. Proceeding to Phase 1 setup.
