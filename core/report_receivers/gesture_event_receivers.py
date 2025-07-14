from kivy.clock import Clock

_callbacks = {
    "on_eyes": None,
    "on_blink": None,
    "on_nod": None,
    "on_yawn": None,
    "on_microsleep": None,
}

def register_callbacks(
    on_eyes=None,
    on_blink=None,
    on_nod=None,
    on_yawn=None,
    on_microsleep=None,
):
    _callbacks["on_eyes"] = on_eyes
    _callbacks["on_blink"] = on_blink
    _callbacks["on_nod"] = on_nod
    _callbacks["on_yawn"] = on_yawn
    _callbacks["on_microsleep"] = on_microsleep
    print("[Receivers] Callbacks registrados desde DriverMonitoringScreen")


def format_blink_report(data: dict) -> str:
    count = data.get("blink_count", "N/A")
    duration = data.get("blink_avg_duration", "N/A")
    comment = data.get("blink_comment", "")
    formatted = (
        f"Reporte:\n"
        f"Total de parpadeos: {count}\n"
        f"Duración promedio: {duration} ms\n"
        f"{comment}"
    )
    return formatted

def format_yawn_report_5min(data: dict) -> str:
    count = data.get("yawn_count", "N/A")
    duration = data.get("avg_duration", "N/A")
    comment = data.get("comment", "")
    formatted = (
        f"Reporte 5 minutos:\n"
        f"Total de bostezos: {count}\n"
        f"Duración promedio: {duration}\n"
        f"{comment}"
    )
    return formatted

def format_yawn_report_10min(data: dict) -> str:
    count = data.get("yawn_count", "N/A")
    duration = data.get("avg_duration", "N/A")
    comment = data.get("comment", "")
    formatted = (
        f"Reporte 10 minutos:\n"
        f"Total de bostezos: {count}\n"
        f"Duración promedio: {duration}\n"
        f"{comment}"
    )
    return formatted

def print_eye_rub_event(message: str):
    full_message = f"[Frotamiento de ojos receivers] {message}"
    if _callbacks["on_eyes"]:
        Clock.schedule_once(lambda dt: _callbacks["on_eyes"](full_message))
    else:
        print(full_message)

def print_nod_event(message: str):
    full_message = f"[Cabeceo receivers] {message}"
    if _callbacks["on_nod"]:
        Clock.schedule_once(lambda dt: _callbacks["on_nod"](full_message))
    else:
        print(full_message)

def print_yawn_event(message: str):
    full_message = f"[Bostezo Detectado receivers] {message}"
    if _callbacks["on_yawn"]:
        Clock.schedule_once(lambda dt: _callbacks["on_yawn"](full_message))
    else:
        print(full_message)

def print_yawn_5min_report_db(data: dict):
    formatted_message = format_yawn_report_5min(data)
    if _callbacks["on_yawn"]:
        Clock.schedule_once(lambda dt: _callbacks["on_yawn"](formatted_message))
    else:
        print(formatted_message)

def print_yawn_10min_report_db(data: dict):
    formatted_message = format_yawn_report_10min(data)
    if _callbacks["on_yawn"]:
        Clock.schedule_once(lambda dt: _callbacks["on_yawn"](formatted_message))
    else:
        print(formatted_message)

def print_microsleep_event(message: str):
    full_message = f"🛌 Microsueño:\n{message}"
    if _callbacks["on_microsleep"]:
        Clock.schedule_once(lambda dt: _callbacks["on_microsleep"](full_message))
    else:
        print(full_message)

def print_minute_report_db(data: dict):
    formatted_message = format_blink_report(data)
    if _callbacks["on_blink"]:
        Clock.schedule_once(lambda dt: _callbacks["on_blink"](formatted_message))
    else:
        print(formatted_message)

def print_blink_event(message: str):
    full_message = f"[Parpadeo receivers] {message}"
    if _callbacks["on_blink"]:
        Clock.schedule_once(lambda dt: _callbacks["on_blink"](full_message))
    else:
        print(full_message)
