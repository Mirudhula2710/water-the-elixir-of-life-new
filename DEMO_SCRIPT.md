# Demo Script - Water Elixir of Life (10 Minutes)

## 1. Introduction (2 mins)
- Briefly introduce the architecture: "This project uses simulated sensors feeding into a multiprocess Python engine. It evaluates readings against a Torricelli physics model and an SVM_RBF ML model in real-time."
- Show the architecture running in one terminal: python run_all.py
- Point to the Flask UI at http://127.0.0.1:5000 to show data flowing.

## 2. Telemetry and Detection Engine (3 mins)
- Trigger a WARNING (TC02): "I'm going to inject a mild abnormal drainage in the Canteen."
- Trigger a CRITICAL leak (TC04): "Now, I'll inject a massive leak into the Hostel Blocks."
- Point out the terminal log: *** CRITICAL ALERT in Hostel Blocks *** Simulated Valve Shutoff executed.
- Highlight the **ML Metrics**: "The ML model was retrained on synthetic data. Accuracy: 0.9850, Macro F1: 0.9356."
  - *If asked about the 99.75% metric:* "That old metric was unverifiable due to data leakage. We dropped the leaking columns and safely achieved 98.5%."

## 3. Web Dashboards (Spring & Angular) (3 mins)
- Open http://localhost:4200 (Angular UI).
- Show the **Dashboard** updating in real-time via RxJS.
- Show the **Alerts Table** and expand the Gemini explanation. Point out how Gemini interprets the deviation safely.
- Resolve the Critical alert as a Staff member: "Resolving this ticket automatically reopens the zone's valve in the database."

## 4. Code & Database Integrity (2 mins)
- Open Postman to show the Spring Boot API (GET /api/alerts).
- Open pp.py to highlight **D12** (Flask Auth in SQLite, telemetry in MySQL via binds).
- Highlight the AlertEvent abstract class in Java to show polymorphism.

## Fallback Answers ("If X fails, say Y")
- **If MySQL fails to connect**: "We have a built-in environment switch. Setting DB_BACKEND=sqlite falls back perfectly to the SQLite database without changing the logic paths."
- **If Gemini times out**: "The system gracefully handles API timeouts with a pre-written fallback template."
- **If Angular fails to compile**: "We can demonstrate the exact same UI workflows in the Flask backend which is guaranteed to run."
