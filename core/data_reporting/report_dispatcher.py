# /Users/kevin/Desktop/tesis/core/data_reporting/report_dispatcher.py

def dispatch_blink_detailed_report(message: str):
    print(f"[BlinkDetailedReport] {message}")

def dispatch_blink_summary_report(message: str):
    print(f"[BlinkSummaryReport] {message}")

def dispatch_eye_rub_detailed_report(message: str):
    print(f"[EyeRubDetailedReport] {message}")

def dispatch_eye_rub_summary_report(message: str):
    print(f"[EyeRubSummaryReport] {message}")

def dispatch_nods_detailed_report(message: str):
    """Envía los reportes detallados de cabeceos a la consola."""
    print(f"[NodsDetailedReport] {message}")

def dispatch_nods_summary_report(message: str):
    """Envía el resumen final de cabeceos a la consola."""
    print(f"[NodsSummaryReport] {message}")

def dispatch_yawn_detailed_report(message: str):
    """Envía los reportes detallados de bostezos a la consola."""
    print(f"[YawnDetailedReport] {message}")

def dispatch_yawn_summary_report(message: str):
    """Envía el resumen final de bostezos a la consola."""
    print(f"[YawnSummaryReport] {message}")