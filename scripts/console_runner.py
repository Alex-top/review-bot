"""
Консольный адаптер для тестирования бота отзывов.
Включает синхронизацию с Яндекс.Диском.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🔍 Загрузка модулей...")

import core.review_bot
print(f"📂 Модуль ReviewBot: {core.review_bot.__file__}")

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
    from storage.yandex_client import YandexDiskClient
    print("✅ YandexDiskClient загружен")
except Exception as e:
    print(f"⚠️ Ошибка загрузки YandexDiskClient: {e}")
    YandexDiskClient = None

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
    
        # === СИНХРОНИЗАЦИЯ С ЯНДЕКС.ДИСКОМ ===
    yandex_token = os.getenv("YANDEX_TOKEN")
    if yandex_token and YandexDiskClient:
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            local_csv = os.path.join(base_dir, "storage", "reviews.csv")
            
            yandex_client = YandexDiskClient(yandex_token, local_csv, "/Отзывы/reviews.csv")
            print("🔄 Синхронизация с Яндекс.Диском...")
            yandex_client.sync_from_cloud()
            yandex_client.sync_to_cloud()
            print("✅ Синхронизация завершена")
        except Exception as e:
            print(f"⚠️ Ошибка синхронизации с Яндекс.Диском: {e}")
            print("   Продолжаем работу без синхронизации...")
    else:
        print("ℹ️ Яндекс.Диск не настроен (токен не найден). Работаем локально.")
    
    print("\n📋 Доступные команды:")
    print("  /add [оценка 1 - 5] [текст] - добавить отзыв (например: /add 5 Отличный сервис!)")
    print("  /list - показать все отзывы")
    print("  /my - показать мои отзывы")
    print("  /stats - статистика")
    print("  /exit - выход")
    print("=" * 50)
    
    user_id = 1
    #user_name = "Тестовый пользователь"
    user_name = input("Введите ваше имя: ") or "Аноним"
    
    while True:
        try:
            command = input("\n👤 Вы: ").strip()
            print(f"🔍 Получена команда: {command}")
            
            if command.lower() == "/exit":
                # Синхронизация перед выходом
                if yandex_token and YandexDiskClient:
                    try:
                        print("🔄 Синхронизация с Яндекс.Диском перед выходом...")
                        yandex_client.sync_to_cloud()
                        print("✅ Синхронизация завершена")
                    except Exception as e:
                        print(f"⚠️ Ошибка синхронизации: {e}")
                print("👋 До свидания!")
                break
            
            if command.startswith("/add "):
                print("🔍 Отладка: команда /add обнаружена")  # ← добавить
                try:
                    parts = command.split(" ", 2)
                    print(f"🔍 Отладка: parts = {parts}")  # ← добавить
                    rating = int(parts[1])
                    text = parts[2] if len(parts) > 2 else ""
                    print(f"🔍 Отладка: rating = {rating}, text = {text}")  # ← добавить
                    review = bot.add_review(user_id, user_name, rating, text)
                    print(f"🔍 Отладка: review = {review}")
                    print(f"🤖 Бот: ✅ Спасибо за отзыв! (ID: {review['id']})")
                    # Синхронизация после добавления отзыва
                    if yandex_token and YandexDiskClient:
                        try:
                            yandex_client.sync_to_cloud()
                            print("🔄 Отзыв синхронизирован с Яндекс.Диском")
                        except Exception as e:
                            print(f"⚠️ Ошибка синхронизации: {e}")
                except ValueError as e:
                    #print(f"🤖 Бот: ❌ Ошибка: {e}")
                    print(f"🤖 Бот: ❌ Ошибка валидации: {e}")
                    print("🤖 Бот: ❌ Неверный формат. Используйте: /add [оценка 1-5] [текст]")
                    print("   Пример: /add 5 Отличный сервис!")
                except KeyError as e:
                    print(f"🤖 Бот: ❌ Ошибка KeyError: {e}")
                    print(f"   review = {review}")
                except Exception as e:
                    print(f"🤖 Бот: ❌ Неизвестная ошибка: {e}")
            
            elif command == "/list":
                reviews = bot.get_all_reviews()
                if not reviews:
                    print("🤖 Бот: 📭 Отзывов пока нет")
                else:
                    print("🤖 Бот: 📋 Все отзывы:")
                    print("=" * 60)
                    for r in reviews:
                        stars = "⭐" * int(r['rating'])
                        print(f"  {stars} ({r['rating']}/5)")
                        print(f"  👤 {r['user_name']}")
                        print(f"  💬 {r['text']}")
                        print(f"  📅 {r['date']}")
                        print("-" * 60)
            
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