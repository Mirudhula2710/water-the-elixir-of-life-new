def to_backend_severity(python_severity):
    """
    D4: Maps the core Python severities to the unified backend VARCHAR severities.
    Normal -> LOW
    Warning -> MEDIUM
    Suspected Leak -> HIGH
    Critical -> CRITICAL
    """
    mapping = {
        'Normal': 'LOW',
        'Warning': 'MEDIUM',
        'Suspected Leak': 'HIGH',
        'Critical': 'CRITICAL'
    }
    return mapping.get(python_severity, 'LOW')

def to_python_severity(backend_severity):
    """ Reverse mapping if ever needed. """
    mapping = {
        'LOW': 'Normal',
        'MEDIUM': 'Warning',
        'HIGH': 'Suspected Leak',
        'CRITICAL': 'Critical'
    }
    return mapping.get(backend_severity, 'Normal')
