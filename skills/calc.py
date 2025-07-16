# calc.py – Nova Jr calculator skill (safe eval sandbox)
import math

query = (globals().get("input") or "").strip()

if not query or query.lower() == "calc":
    result = "Please say something like: calc 3 + 4 * 2"
else:
    try:
        expr = query
        if expr.lower().startswith("calc "):
            expr = expr[5:]
        # Sandboxed eval scope
        safe_globals = {
            "__builtins__": {},
            "abs": abs, "round": round, "min": min, "max": max,
            "pow": pow, "sum": sum, "len": len,
            "math": math,
            "pi": math.pi, "e": math.e,
            "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4,
        }
        result = f"{expr.strip()} = {eval(expr, safe_globals)}"
    except Exception as e:
        result = f"❌ Calculation error: {e}"
