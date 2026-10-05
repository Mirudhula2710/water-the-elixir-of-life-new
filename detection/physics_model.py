import sympy as sp

# A_hole / A_tank ratio for simulation purposes
AREA_RATIO = 0.005
GRAVITY = 9.81

# Pre-compute the symbolic expression and lambdify it for fast runtime execution
# Torricelli's law: dh/dt = -(A_hole / A_tank) * sqrt(2 * g * h)
_h0 = sp.Symbol('h0', real=True, positive=True)
_dt = sp.Symbol('dt', real=True, positive=True)
_k = AREA_RATIO * sp.sqrt(2 * GRAVITY)

# Analytical solution for h(t): h(t) = (sqrt(h0) - k*t/2)^2
_h_expr = (sp.sqrt(_h0) - (_k * _dt) / 2)**2

# Create a fast numerical function from the sympy expression
_compute_fast = sp.lambdify((_h0, _dt), _h_expr, modules='numpy')

def compute_expected_drainage(h0, dt):
    """
    Computes the expected tank level after time dt given initial level h0.
    Implements Torricelli's law using a lambdified SymPy expression.
    """
    if h0 <= 0:
        return 0.0
        
    new_h = float(_compute_fast(h0, dt))
    
    # Check if tank emptied completely during dt
    # If the inner term (sqrt(h0) - k*dt/2) becomes negative, the squared result would incorrectly increase.
    # We check if sqrt(h0) < k*dt/2
    k_val = AREA_RATIO * (2 * GRAVITY)**0.5
    if h0**0.5 < (k_val * dt) / 2:
        return 0.0
        
    return new_h
