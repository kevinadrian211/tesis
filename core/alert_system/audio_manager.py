import os
import pygame
import threading
import time
from typing import Optional

class AudioManager:
    """
    Gestor centralizado de audio para el sistema de alertas
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AudioManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.pygame_initialized = False
            self.alarm_thread = None
            self.alarm_playing = False
            self.alarm_lock = threading.Lock()
            self._init_pygame()
    
    def _init_pygame(self):
        """Inicializa pygame mixer si no está inicializado"""
        try:
            if not self.pygame_initialized:
                pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
                pygame.mixer.init()
                self.pygame_initialized = True
                print("[AUDIO] Pygame mixer inicializado correctamente")
        except Exception as e:
            print(f"[ERROR] No se pudo inicializar pygame mixer: {e}")
            self.pygame_initialized = False
    
    def _get_sound_path(self, sound_file: str) -> str:
        """Obtiene la ruta completa del archivo de sonido desde la carpeta sounds"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sounds_dir = os.path.join(current_dir, "sounds")
        return os.path.join(sounds_dir, sound_file)

    def play_notification_sound(self) -> bool:
        """
        Reproduce el sonido de notificación (notification.mp3)
        Retorna True si se reprodujo correctamente, False en caso contrario
        """
        return self._play_sound("notification.mp3", loop=False)
    
    def start_alarm_sound(self) -> bool:
        """
        Inicia la reproducción de la alarma en bucle (alarm.mp3)
        Retorna True si se inició correctamente, False en caso contrario
        """
        with self.alarm_lock:
            if self.alarm_playing:
                print("[ALARMA] La alarma ya está sonando")
                return True
            
            sound_path = self._get_sound_path("alarm.mp3")
            if not os.path.exists(sound_path):
                print(f"[ERROR] No se encontró el archivo de sonido: {sound_path}")
                return False
            
            self.alarm_playing = True
            self.alarm_thread = threading.Thread(
                target=self._play_alarm_loop,
                args=(sound_path,),
                daemon=True
            )
            self.alarm_thread.start()
            print(f"[ALARMA] Iniciando alarma en bucle: {sound_path}")
            return True
    
    def stop_alarm_sound(self):
        """Detiene la reproducción de la alarma"""
        with self.alarm_lock:
            if self.alarm_playing:
                self.alarm_playing = False
                print("[ALARMA] Alarma detenida por el usuario")
            else:
                print("[ALARMA] No hay alarma reproduciéndose")
    
    def is_alarm_playing(self) -> bool:
        """Verifica si la alarma está sonando actualmente"""
        return self.alarm_playing
    
    def toggle_alarm(self):
        """Alterna el estado de la alarma (parar/iniciar)"""
        if self.alarm_playing:
            self.stop_alarm_sound()
        else:
            self.start_alarm_sound()
    
    def reset_alarm_system(self):
        """Reinicia completamente el sistema de alarmas"""
        with self.alarm_lock:
            self.alarm_playing = False
            if self.alarm_thread and self.alarm_thread.is_alive():
                self.alarm_thread.join(timeout=1.0)
            self.alarm_thread = None
            print("[ALARMA] Sistema de alarmas reiniciado")
    
    def _play_sound(self, sound_file: str, loop: bool = False) -> bool:
        """
        Reproduce un archivo de sonido
        Args:
            sound_file: nombre del archivo de sonido
            loop: si debe reproducirse en bucle
        """
        if not self.pygame_initialized:
            print("[ERROR] Pygame mixer no está inicializado")
            return False
        
        sound_path = self._get_sound_path(sound_file)
        
        if not os.path.exists(sound_path):
            print(f"[ERROR] Archivo de sonido no encontrado: {sound_path}")
            return False
        
        try:
            sound = pygame.mixer.Sound(sound_path)
            if loop:
                sound.play(-1)  # -1 significa bucle infinito
            else:
                sound.play()
            print(f"[SONIDO] Reproduciendo: {sound_path}")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo reproducir el sonido {sound_file}: {e}")
            return False
    
    def _play_alarm_loop(self, sound_path: str):
        """
        Reproduce el sonido de alarma en bucle hasta que se detenga
        """
        try:
            if not os.path.exists(sound_path):
                print(f"[ERROR] Archivo de sonido no encontrado: {sound_path}")
                return
            
            alarm_sound = pygame.mixer.Sound(sound_path)
            
            while self.alarm_playing:
                alarm_sound.play()
                sound_length = alarm_sound.get_length()
                time.sleep(sound_length)
        except Exception as e:
            print(f"[ERROR] Error en bucle de alarma: {e}")
            with self.alarm_lock:
                self.alarm_playing = False
    
    def get_alarm_status(self) -> dict:
        """Retorna el estado actual de la alarma"""
        return {
            'playing': self.alarm_playing,
            'thread_alive': self.alarm_thread.is_alive() if self.alarm_thread else False,
            'pygame_initialized': self.pygame_initialized
        }
    
    def cleanup(self):
        """Limpia recursos de audio"""
        self.stop_alarm_sound()
        if self.pygame_initialized:
            try:
                pygame.mixer.quit()
                self.pygame_initialized = False
                print("[AUDIO] Pygame mixer finalizado")
            except Exception as e:
                print(f"[ERROR] Error al finalizar pygame mixer: {e}")

# Instancia global del gestor de audio
audio_manager = AudioManager()
