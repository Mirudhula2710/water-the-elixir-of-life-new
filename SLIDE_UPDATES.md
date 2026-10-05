# Slide Deck Corrections

1. **Architecture/Tech Stack Slide**: 
   - Remove "Tkinter". Add "Flask Dashboard" and "Angular 18 Frontend".
   - Add "Spring Boot 3 (Java 17)" as the REST API backend.
2. **Algorithm Slide**:
   - Remove "Accuracy: 99.75%".
   - Update to: "Accuracy: 98.50%, Macro F1: 0.9356 (Tested on Synthetic Data)".
   - Add note: Final severity is the maximum of the Torricelli Physics Output and the SVM_RBF model.
3. **Use Cases/Testing Slide**:
   - Update TC02 description from whatever it was to: "Mild abnormal drainage -> Warning".
4. **Data Management Slide**:
   - Mention that User Auth remains securely isolated in SQLite (stateless HTTP Basic), while Telemetry resides in 3NF MySQL.
