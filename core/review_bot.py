"""
Ядро бота для сбора отзывов.
Содержит всю бизнес-логику, не зависит от платформы.
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class ReviewBot:
    """Основной класс для работы с отзывами"""
    
    #def __init__(self, csv_file: str = "storage/reviews.csv"):
        #self.csv_file = csv_file
        #self._ensure_file_exists()
    
    #import os

class ReviewBot:
    def __init__(self, csv_file: str = None):
        # Если путь не указан — используем путь по умолчанию
        if csv_file is None:
            # Определяем путь к папке storage относительно текущего файла
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_file = os.path.join(base_dir, "storage", "reviews.csv")
        
        self.csv_file = csv_file
        
        # Убеждаемся, что папка storage существует
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """
        Проверяет, что CSV-файл существует и содержит правильные заголовки.
        Если файла нет, он пуст или заголовки неверные — создаёт/исправляет.
        """
        required_headers = ['id', 'user_id', 'user_name', 'rating', 'text', 'date', 'status']
        
        need_create = False
        
        # 1. Проверяем, существует ли файл
        if not os.path.exists(self.csv_file):
            print(f"📁 Файл {self.csv_file} не найден. Создаю...")
            need_create = True
        else:
            # 2. Проверяем, есть ли в файле заголовки
            try:
                with open(self.csv_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    
                    # Если файл пустой или заголовки не совпадают
                    if not first_line:
                        print(f"⚠️ Файл {self.csv_file} пуст. Добавляю заголовки...")
                        need_create = True
                    elif not all(header in first_line for header in required_headers):
                        print(f"⚠️ Файл {self.csv_file} содержит неверные заголовки. Исправляю...")
                        need_create = True
            except Exception as e:
                print(f"⚠️ Ошибка чтения файла: {e}. Пересоздаю...")
                need_create = True
        
        # 3. Создаём или пересоздаём файл с правильными заголовками
        if need_create:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(required_headers)
            print(f"✅ Файл {self.csv_file} создан с заголовками")
        else:
            print(f"✅ Файл {self.csv_file} в порядке")
    
    def _get_next_id(self) -> int:
        """Возвращает следующий ID для нового отзыва"""
        reviews = self.get_all_reviews()
        if not reviews:
            return 1
        return max(int(r['id']) for r in reviews) + 1
    
    def get_all_reviews(self) -> List[Dict[str, str]]:
        """Возвращает все отзывы в виде списка словарей"""
        reviews = []
        if not os.path.exists(self.csv_file):
            return reviews
        
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                reviews.append(row)
        return reviews
    
    def add_review(self, user_id: int, user_name: str, rating: int, text: str) -> Dict[str, str]:
        """Добавляет новый отзыв"""
        if not text or len(text.strip()) < 3:
            raise ValueError("Текст отзыва должен содержать минимум 3 символа")
        if rating < 1 or rating > 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        
        review = {
            'id': str(self._get_next_id()),
            'user_id': str(user_id),
            'user_name': user_name or str(user_id),
            'rating': str(rating),
            'text': text.strip(),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'new'
        }

        print(f"🔍 Отладка: review = {review}")  #

        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'user_id', 'user_name', 'rating', 'text', 'date', 'status'])
            writer.writerow(review)
        
        return review
    
    def get_user_reviews(self, user_id: int) -> List[Dict[str, str]]:
        """Возвращает все отзывы конкретного пользователя"""
        all_reviews = self.get_all_reviews()
        return [r for r in all_reviews if int(r['user_id']) == user_id]
    
    def update_status(self, review_id: int, new_status: str) -> bool:
        """
        Обновляет статус отзыва.
        Возвращает True, если обновление выполнено.
        """
        if new_status not in ['new', 'processed', 'archived']:
            raise ValueError("Статус должен быть: new, processed, archived")
        
        reviews = self.get_all_reviews()
        updated = False
        
        for i, review in enumerate(reviews):
            if int(review['id']) == review_id:
                reviews[i]['status'] = new_status
                updated = True
                break
        
        if updated:
            # Перезаписываем весь CSV
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'user_id', 'user_name', 'rating', 'text', 'date', 'status'])
                writer.writeheader()
                writer.writerows(reviews)
        
        return updated
    
    def get_statistics(self) -> Dict[str, any]:
        """Возвращает статистику по отзывам"""
        reviews = self.get_all_reviews()
        if not reviews:
            return {'total': 0, 'avg_rating': 0, 'by_status': {}}
        
        total = len(reviews)
        avg_rating = sum(int(r['rating']) for r in reviews) / total
        
        by_status = {}
        for r in reviews:
            status = r['status']
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            'total': total,
            'avg_rating': round(avg_rating, 1),
            'by_status': by_status
        }