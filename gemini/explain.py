import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def explain_alert(zone_name, severity, deviation):
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Simulated explanation for presentation purposes if no key is provided
    if not api_key or api_key == "your_key_here":
        if severity == "Critical":
            return f"A critical deviation of {deviation:.2f} liters indicates abnormal, high-volume water loss in the {zone_name} that strongly points to an active pipe rupture, failed fixture, or stuck open valve. Immediately dispatch a technician to inspect supply lines and equipment, and isolate the local zone shutoff valve if uncontrolled flow or pooling water is detected."
        else:
            return f"This alert indicates that the {zone_name} is losing roughly {deviation:.2f} liters of water beyond our baseline hydraulic model, pointing to an active leak or continuously running fixture. Please dispatch a technician immediately to inspect restrooms and mechanical rooms, and isolate zone shut-off valves if necessary to locate the source."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
    prompt = f"You are an expert facilities management assistant for a campus water system. An alert has been generated for the {zone_name}. Severity: {severity}. Deviation: {deviation:.2f} liters/level. Provide a short, human-readable explanation of what this means and suggest 1-2 immediate maintenance actions. Keep it under 3 sentences."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback simulation if rate limit exceeded during presentation
        if severity == "Critical":
            return f"A critical deviation of {deviation:.2f} liters indicates abnormal, high-volume water loss in the {zone_name} that strongly points to an active pipe rupture, failed fixture, or stuck open valve. Immediately dispatch a technician to inspect supply lines and equipment, and isolate the local zone shutoff valve if uncontrolled flow or pooling water is detected."
        else:
            return f"This alert indicates that the {zone_name} is losing roughly {deviation:.2f} liters of water beyond our baseline hydraulic model, pointing to an active leak or continuously running fixture. Please dispatch a technician immediately to inspect restrooms and mechanical rooms, and isolate zone shut-off valves if necessary to locate the source."
