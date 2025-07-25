#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento de todas las alertas
del sistema de monitoreo de fatiga del conductor.
"""

import time
import threading
from typing import Dict, Any

# Importar todos los módulos de alertas
try:
    import blink_alert
    import eye_rub_alert
    import microsleep_alert
    import nod_alert
    import yawn_5min_alert
    import yawn_10min_alert
    import yawn_alert
    from audio_manager import audio_manager
    
    print("✓ Todos los módulos importados correctamente")
except ImportError as e:
    print(f"✗ Error importando módulos: {e}")
    exit(1)

class AlertTester:
    """Clase para probar todas las funcionalidades de alerta"""
    
    def __init__(self):
        self.test_results = {}
        self.alarm_test_duration = 3  # segundos para probar la alarma
    
    def print_header(self, title: str):
        """Imprime un encabezado formateado"""
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    
    def print_test(self, test_name: str):
        """Imprime el nombre de la prueba actual"""
        print(f"\n[PRUEBA] {test_name}")
        print("-" * 40)
    
    def wait_for_user(self, message: str = "Presiona Enter para continuar..."):
        """Espera input del usuario"""
        input(f"\n{message}")
    
    def test_audio_manager(self):
        """Prueba las funciones básicas del audio manager"""
        self.print_test("Audio Manager - Funciones básicas")
        
        # Verificar inicialización
        status = audio_manager.get_alarm_status()
        print(f"Estado inicial: {status}")
        
        # Probar sonido de notificación
        print("Probando sonido de notificación...")
        result = audio_manager.play_notification_sound()
        print(f"Resultado reproducción notificación: {result}")
        
        time.sleep(1)
        
        # Probar alarma
        print("Iniciando alarma de prueba...")
        alarm_result = audio_manager.start_alarm_sound()
        print(f"Resultado inicio alarma: {alarm_result}")
        
        if alarm_result:
            print(f"Alarma sonará por {self.alarm_test_duration} segundos...")
            time.sleep(self.alarm_test_duration)
            
            print("Deteniendo alarma...")
            audio_manager.stop_alarm_sound()
            
            # Verificar que se detuvo
            time.sleep(0.5)
            is_playing = audio_manager.is_alarm_playing()
            print(f"¿Alarma aún reproduciéndose?: {is_playing}")
        
        self.test_results['audio_manager'] = True
    
    def test_blink_alert(self):
        """Prueba las alertas de parpadeo"""
        self.print_test("Blink Alert - Alertas de parpadeo")
        
        # Datos de prueba con comentarios de riesgo
        test_data = [
            {"blink_comment": "fatiga detectada"},
            {"blink_comment": "señales de cansancio"},
            {"blink_comment": "alto riesgo de somnolencia"},
            {"blink_comment": "normal"}  # Este no debería disparar alerta
        ]
        
        for i, data in enumerate(test_data, 1):
            print(f"Prueba {i}: {data}")
            blink_alert.handle_blink_minute_report(data)
            time.sleep(1)
        
        self.test_results['blink_alert'] = True
    
    def test_eye_rub_alert(self):
        """Prueba las alertas de frotamiento de ojos"""
        self.print_test("Eye Rub Alert - Frotamiento de ojos")
        
        test_messages = [
            "Frotamiento de ojos detectado - nivel bajo",
            "Frotamiento frecuente de ojos - posible fatiga",
            "Múltiples eventos de frotamiento detectados"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"Prueba {i}: {message}")
            eye_rub_alert.handle_eye_rub_event(message)
            time.sleep(1)
        
        self.test_results['eye_rub_alert'] = True
    
    def test_nod_alert(self):
        """Prueba las alertas de cabeceo"""
        self.print_test("Nod Alert - Cabeceo detectado")
        
        test_messages = [
            "Cabeceo leve detectado",
            "Cabeceo pronunciado - atención requerida",
            "Múltiples eventos de cabeceo"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"Prueba {i}: {message}")
            nod_alert.handle_nod_event(message)
            time.sleep(1)
        
        self.test_results['nod_alert'] = True
    
    def test_yawn_alerts(self):
        """Prueba todas las alertas de bostezo"""
        self.print_test("Yawn Alerts - Alertas de bostezo")
        
        # Prueba yawn_alert simple
        print("1. Yawn Alert simple:")
        yawn_messages = [
            "Bostezo detectado",
            "Bostezo prolongado detectado"
        ]
        
        for message in yawn_messages:
            print(f"   - {message}")
            yawn_alert.handle_yawn_event(message)
            time.sleep(1)
        
        # Prueba yawn_5min_alert
        print("\n2. Yawn 5min Alert:")
        yawn_5min_data = [
            {"comment": "anormal"},
            {"comment": "posible fatiga"},
            {"comment": "normal"}  # No debería disparar
        ]
        
        for data in yawn_5min_data:
            print(f"   - {data}")
            yawn_5min_alert.handle_yawn_5min_report(data)
            time.sleep(1)
        
        # Prueba yawn_10min_alert
        print("\n3. Yawn 10min Alert:")
        yawn_10min_data = [
            {"comment": "fatiga detectada"},
            {"comment": "cansancio evidente"},
            {"comment": "normal"}  # No debería disparar
        ]
        
        for data in yawn_10min_data:
            print(f"   - {data}")
            yawn_10min_alert.handle_yawn_10min_report(data)
            time.sleep(1)
        
        self.test_results['yawn_alerts'] = True
    
    def test_microsleep_alert(self):
        """Prueba las alertas de microsueño (con alarma)"""
        self.print_test("Microsleep Alert - Alerta crítica con alarma")
        
        print("⚠️  ATENCIÓN: Esta prueba activará la alarma de emergencia")
        self.wait_for_user("Presiona Enter cuando estés listo para la alarma...")
        
        # Activar microsueño
        microsleep_alert.handle_microsleep_event("MICROSUEÑO DETECTADO - PELIGRO INMEDIATO")
        
        print(f"Alarma sonará por {self.alarm_test_duration} segundos...")
        time.sleep(self.alarm_test_duration)
        
        # Probar funciones de control de alarma
        print("\nProbando funciones de control de alarma:")
        
        print("- Estado actual:", microsleep_alert.get_alarm_status())
        print("- ¿Alarma sonando?:", microsleep_alert.is_alarm_playing())
        
        print("- Deteniendo alarma...")
        microsleep_alert.stop_alarm_sound()
        
        time.sleep(0.5)
        print("- ¿Alarma sonando después de detener?:", microsleep_alert.is_alarm_playing())
        
        # Probar toggle
        print("- Probando toggle de alarma...")
        microsleep_alert.toggle_alarm()
        time.sleep(1)
        print("- ¿Alarma sonando después de toggle?:", microsleep_alert.is_alarm_playing())
        
        # Detener definitivamente
        microsleep_alert.stop_alarm_sound()
        
        # Probar reset del sistema
        print("- Reiniciando sistema de alarmas...")
        microsleep_alert.reset_alarm_system()
        
        self.test_results['microsleep_alert'] = True
    
    def test_interactive_mode(self):
        """Modo interactivo para probar alertas manualmente"""
        self.print_test("Modo Interactivo")
        
        while True:
            print("\nOpciones disponibles:")
            print("1. Probar notificación simple")
            print("2. Probar alarma de microsueño")
            print("3. Detener alarma")
            print("4. Estado de la alarma")
            print("5. Toggle alarma")
            print("6. Reset sistema de alarmas")
            print("0. Salir del modo interactivo")
            
            try:
                choice = input("\nSelecciona una opción (0-6): ").strip()
                
                if choice == "0":
                    break
                elif choice == "1":
                    audio_manager.play_notification_sound()
                    print("✓ Sonido de notificación reproducido")
                elif choice == "2":
                    microsleep_alert.handle_microsleep_event("Prueba manual de microsueño")
                    print("✓ Alarma de microsueño activada")
                elif choice == "3":
                    audio_manager.stop_alarm_sound()
                    print("✓ Alarma detenida")
                elif choice == "4":
                    status = audio_manager.get_alarm_status()
                    print(f"Estado: {status}")
                elif choice == "5":
                    audio_manager.toggle_alarm()
                    is_playing = audio_manager.is_alarm_playing()
                    print(f"✓ Toggle realizado. ¿Sonando?: {is_playing}")
                elif choice == "6":
                    audio_manager.reset_alarm_system()
                    print("✓ Sistema reiniciado")
                else:
                    print("Opción no válida")
                    
            except KeyboardInterrupt:
                print("\nSaliendo del modo interactivo...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def print_results(self):
        """Imprime el resumen de resultados de las pruebas"""
        self.print_header("RESUMEN DE PRUEBAS")
        
        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())
        
        print(f"Total de pruebas: {total_tests}")
        print(f"Pruebas exitosas: {passed_tests}")
        print(f"Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\nDetalle por módulo:")
        for test_name, result in self.test_results.items():
            status = "✓ PASÓ" if result else "✗ FALLÓ"
            print(f"  {test_name}: {status}")
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        self.print_header("INICIANDO PRUEBAS DEL SISTEMA DE ALERTAS")
        
        try:
            # Pruebas básicas
            self.test_audio_manager()
            self.wait_for_user()
            
            self.test_blink_alert()
            self.wait_for_user()
            
            self.test_eye_rub_alert()
            self.wait_for_user()
            
            self.test_nod_alert()
            self.wait_for_user()
            
            self.test_yawn_alerts()
            self.wait_for_user()
            
            # Prueba crítica (con alarma)
            self.test_microsleep_alert()
            self.wait_for_user()
            
            # Modo interactivo opcional
            print("\n¿Deseas entrar al modo interactivo para pruebas manuales?")
            if input("(s/n): ").lower().startswith('s'):
                self.test_interactive_mode()
            
            # Mostrar resultados
            self.print_results()
            
        except KeyboardInterrupt:
            print("\n\nPruebas interrumpidas por el usuario")
            audio_manager.stop_alarm_sound()
        except Exception as e:
            print(f"\nError durante las pruebas: {e}")
            audio_manager.stop_alarm_sound()
        finally:
            # Limpieza final
            print("\nLimpiando recursos...")
            audio_manager.cleanup()
            print("✓ Limpieza completada")

def main():
    """Función principal"""
    print("🚗 SISTEMA DE PRUEBAS - MONITOR DE FATIGA DEL CONDUCTOR")
    print("=" * 60)
    
    # Verificar dependencias
    try:
        import plyer
        import pygame
        print("✓ Dependencias verificadas (plyer, pygame)")
    except ImportError as e:
        print(f"✗ Dependencias faltantes: {e}")
        print("Instala con: pip install plyer pygame")
        return
    
    # Crear y ejecutar pruebas
    tester = AlertTester()
    
    print("\nOpciones:")
    print("1. Ejecutar todas las pruebas automáticamente")
    print("2. Modo interactivo solamente")
    print("3. Salir")
    
    try:
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == "1":
            tester.run_all_tests()
        elif choice == "2":
            tester.test_interactive_mode()
        elif choice == "3":
            print("Saliendo...")
        else:
            print("Opción no válida")
            
    except KeyboardInterrupt:
        print("\nPrograma interrumpido")
    finally:
        # Asegurar limpieza
        audio_manager.stop_alarm_sound()
        audio_manager.cleanup()

if __name__ == "__main__":
    main()