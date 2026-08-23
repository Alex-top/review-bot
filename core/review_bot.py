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
    
    def __init__(self, csv_file: str = "storage/reviews.csv"):
        self.csv_file = csv_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Создаёт CSV-файл с заголовками, если он не существует"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'user_id', 'user_name', 'rating', 'text', 'date', 'status'])
    
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
        """
        Добавляет новый отзыв.
        Возвращает добавленный отзыв в виде словаря.
        """
        # Валидация
        if not text or len(text.strip()) < 3:
            raise ValueError("Текст отзыва должен содержать минимум 3 символа")
        if rating < 1 or rating > 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        
        # Формируем запись
        review = {
            'id': str(self._get_next_id()),
            'user_id': str(user_id),
            'user_name': user_name or str(user_id),
            'rating': str(rating),
            'text': text.strip(),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'new'
        }
        
        # Добавляем в CSV
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