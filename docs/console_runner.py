"""
Консольный адаптер для тестирования бота отзывов (упрощённая версия).
"""

import sys
import os

# Добавляем путь к корню проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🔍 Загрузка модулей...")

try:
    from core.review_bot import ReviewBot
    print("✅ ReviewBot загружен")
except Exception as e:
    print(f"❌ Ошибка загрузки ReviewBot: {e}")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env загружен")
except Exception as e:
    print(f"⚠️ Ошибка загрузки .env: {e}")

print("🔍 Запуск основного цикла...")

def main():
    print("🛒 Запуск бота для сбора отзывов (консольный режим)")
    print("=" * 50)
    
    try:
        bot = ReviewBot()
        print("✅ Бот инициализирован")
    except Exception as e:
        print(f"❌ Ошибка инициализации бота: {e}")
        return
    
    print("\n📋 Доступные команды:")
    print("  /add [оценка] [текст] - добавить отзыв (например: /add 5 Отличный сервис!)")
    print("  /list - показать все отзывы")
    print("  /my - показать мои отзывы")
    print("  /stats - статистика")
    print("  /exit - выход")
    print("=" * 50)
    
    user_id = 1
    user_name = "Тестовый пользователь"
    
    while True:
        try:
            command = input("\n👤 Вы: ").strip()
            print(f"🔍 Получена команда: {command}")
            
            if command.lower() == "/exit":
                print("👋 До свидания!")
                break
            
            if command.startswith("/add "):
                try:
                    parts = command.split(" ", 2)
                    rating = int(parts[1])
                    text = parts[2] if len(parts) > 2 else ""
                    review = bot.add_review(user_id, user_name, rating, text)
                    print(f"🤖 Бот: ✅ Спасибо за отзыв! (ID: {review['id']})")
                except ValueError as e:
                    print(f"🤖 Бот: ❌ Ошибка: {e}")
                except Exception as e:
                    print(f"🤖 Бот: ❌ Ошибка: {e}")
            
            elif command == "/list":
                reviews = bot.get_all_reviews()
                if not reviews:
                    print("🤖 Бот: 📭 Отзывов пока нет")
                else:
                    print("🤖 Бот: 📋 Все отзывы:")
                    for r in reviews:
                        print(f"  ID {r['id']} | {r['user_name']} | {r['rating']}⭐ | {r['text']} | {r['status']}")
            
            elif command == "/my":
                reviews = bot.get_user_reviews(user_id)
                if not reviews:
                    print("🤖 Бот: 📭 У вас пока нет отзывов")
                else:
                    print("🤖 Бот: 📋 Ваши отзывы:")
                    for r in reviews:
                        print(f"  ID {r['id']} | {r['rating']}⭐ | {r['text']}")
            
            elif command == "/stats":
                stats = bot.get_statistics()
                print(f"🤖 Бот: 📊 Статистика:")
                print(f"  Всего отзывов: {stats['total']}")
                print(f"  Средняя оценка: {stats['avg_rating']}")
                print(f"  По статусам: {stats['by_status']}")
            
            elif command == "":
                # Пустой ввод — ничего не делаем
                pass
            
            else:
                print("🤖 Бот: ❓ Неизвестная команда. Используйте /add, /list, /my, /stats, /exit")
        
        except EOFError:
            print("\n👋 Ввод завершён. До свидания!")
            break
        except KeyboardInterrupt:
            print("\n👋 Прервано пользователем. До свидания!")
            break
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    print("🔍 Скрипт дошел до __main__")
    main()
    print("🔍 Скрипт завершил работу")