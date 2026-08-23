"""
Клиент для работы с Яндекс.Диском.
Синхронизирует локальный CSV-файл с облаком.
"""

import os
import yadisk
from typing import Optional

class YandexDiskClient:
    """Клиент для Яндекс.Диска"""
    
    def __init__(self, token: str, local_file: str, remote_path: str):
        self.token = token
        self.local_file = local_file
        self.remote_path = remote_path
        self.client = yadisk.Client(token=token)
    
    def sync_to_cloud(self) -> bool:
        """
        Загружает локальный CSV-файл на Яндекс.Диск.
        Возвращает True, если успешно.
        """
        try:
            # Проверяем, что токен работает
            if not self.client.check_token():
                print("❌ Невалидный токен Яндекс.Диска")
                return False
            
            # Убеждаемся, что папка существует
            remote_dir = os.path.dirname(self.remote_path)
            if remote_dir and not self.client.exists(remote_dir):
                self.client.mkdir(remote_dir)
                print(f"📁 Создана папка {remote_dir}")
            
            # Загружаем файл
            print(f"📤 Загружаю файл {self.local_file} в {self.remote_path}")
            print(f"📂 Полный путь на диске: {self.remote_path}")
            
            self.client.upload(self.local_file, self.remote_path, overwrite=True)
            print(f"✅ Файл {self.local_file} загружен в {self.remote_path}")
            return True
        
        except Exception as e:
            print(f"❌ Ошибка синхронизации с Яндекс.Диском: {e}")
            return False
    
    def sync_from_cloud(self) -> bool:
        """
        Загружает файл с Яндекс.Диска локально.
        Возвращает True, если успешно.
        """
        try:
            if not self.client.check_token():
                print("❌ Невалидный токен Яндекс.Диска")
                return False
            
            # Проверяем, что файл существует на диске
            if not self.client.exists(self.remote_path):
                print(f"⚠️ Файл {self.remote_path} не найден на Яндекс.Диске")
                return False
            
            # Скачиваем файл
            self.client.download(self.remote_path, self.local_file)
            print(f"✅ Файл {self.remote_path} загружен локально")
            return True
        
        except Exception as e:
            print(f"❌ Ошибка синхронизации с Яндекс.Диска: {e}")
            return False