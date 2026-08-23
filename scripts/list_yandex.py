"""
Показывает содержимое корня Яндекс.Диска.
Помогает проверить, что папка /Отзывы действительно создалась.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from storage.yandex_client import YandexDiskClient


def main():
    token = os.getenv("YANDEX_TOKEN")
    if not token:
        print("❌ YANDEX_TOKEN не найден в .env")
        return
    
    print("🔍 Подключение к Яндекс.Диску...")
    client = YandexDiskClient(token, "storage/reviews.csv", "/Отзывы/reviews.csv")
    
    if not client.client.check_token():
        print("❌ Токен невалидный")
        return
    
    print("✅ Токен валидный")
    print("\n📂 Содержимое корня Яндекс.Диска:")
    print("-" * 40)
    
    try:
        items = client.client.listdir("/")
        if not items:
            print("📭 Корень пуст")
        else:
            for item in items:
                name = item['name']
                if item['type'] == 'dir':
                    print(f"📁 {name}/")
                else:
                    size = item.get('size', 0)
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024 * 1024:
                        size_str = f"{size // 1024} KB"
                    else:
                        size_str = f"{size // (1024 * 1024)} MB"
                    print(f"📄 {name} ({size_str})")
        
        # Проверяем наличие папки Отзывы
        print("\n" + "-" * 40)
        exists = client.client.exists("/Отзывы")
        print(f"🔍 Папка '/Отзывы' существует: {'✅ Да' if exists else '❌ Нет'}")
        
        if exists:
            print("\n📂 Содержимое папки /Отзывы:")
            items = client.client.listdir("/Отзывы")
            if not items:
                print("   📭 Папка пуста")
            else:
                for item in items:
                    print(f"   📄 {item['name']}")
    
    except Exception as e:
        print(f"❌ Ошибка при получении списка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()