#!/usr/bin/env python3
"""
Клиент для работы с Fireflies.ai API
Документация API: https://docs.fireflies.ai/graphql-api/
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class FirefliesClient:
    """Клиент для взаимодействия с Fireflies.ai API"""

    API_URL = "https://api.fireflies.ai/graphql"

    def __init__(self, api_key: Optional[str] = None, config_path: Optional[str] = None):
        """
        Инициализация клиента

        Args:
            api_key: API ключ Fireflies. Если не указан, берется из переменной окружения FIREFLIES_API_KEY
            config_path: Путь к файлу конфигурации. По умолчанию config.json в текущей директории
        """
        self.api_key = api_key or os.getenv("FIREFLIES_API_KEY")
        if not self.api_key:
            print("⚠️  FIREFLIES_API_KEY не установлен. Получите ключ на https://app.fireflies.ai/integrations/custom/fireflies")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Загружаем конфигурацию
        config_file = config_path or (Path(__file__).parent / "config.json")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"✅ Конфигурация загружена: {config_file}")
        except FileNotFoundError:
            print(f"⚠️  Файл конфигурации не найден: {config_file}")
            self.config = {"team_members": [], "keywords": []}

        # Создаем папки для хранения данных
        self.base_dir = Path(__file__).parent / "meetings"
        self.transcripts_dir = self.base_dir / "transcripts"
        self.processed_dir = self.base_dir / "processed"

        for dir_path in [self.transcripts_dir, self.processed_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def _execute_query(self, query: str, variables: Dict = None) -> Dict:
        """
        Выполнение GraphQL запроса

        Args:
            query: GraphQL запрос
            variables: Переменные для запроса

        Returns:
            Ответ от API
        """
        if not self.api_key:
            raise ValueError("API ключ не установлен. Установите переменную окружения FIREFLIES_API_KEY")

        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(
            self.API_URL,
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    def get_recent_transcripts(self, limit: int = 10) -> List[Dict]:
        """
        Получить последние транскрипты

        Args:
            limit: Количество транскриптов для получения

        Returns:
            Список транскриптов
        """
        query = """
        query Transcripts($limit: Int!) {
            transcripts(limit: $limit) {
                id
                title
                date
                duration
                organizer_email
                participants
                transcript_url
                video_url
                audio_url
                sentences {
                    text
                    speaker_name
                    start_time
                    end_time
                }
                summary {
                    keywords
                    action_items
                    outline
                    shorthand_bullet
                    overview
                }
            }
        }
        """

        result = self._execute_query(query, {"limit": limit})
        return result.get("data", {}).get("transcripts", [])

    def get_transcript_by_id(self, transcript_id: str) -> Optional[Dict]:
        """
        Получить транскрипт по ID

        Args:
            transcript_id: ID транскрипта

        Returns:
            Данные транскрипта или None
        """
        query = """
        query Transcript($id: String!) {
            transcript(id: $id) {
                id
                title
                date
                duration
                organizer_email
                participants
                transcript_url
                video_url
                audio_url
                sentences {
                    text
                    speaker_name
                    start_time
                    end_time
                }
                summary {
                    keywords
                    action_items
                    outline
                    shorthand_bullet
                    overview
                }
            }
        }
        """

        result = self._execute_query(query, {"id": transcript_id})
        return result.get("data", {}).get("transcript")

    def save_transcript(self, transcript: Dict) -> Path:
        """
        Сохранить транскрипт в файл

        Args:
            transcript: Данные транскрипта

        Returns:
            Путь к сохраненному файлу
        """
        # Форматируем дату для имени файла
        date_str = transcript.get("date", datetime.now().isoformat())
        try:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            filename = f"{date_obj.strftime('%Y-%m-%d')}_{transcript['id']}.json"
        except:
            filename = f"{transcript['id']}.json"

        filepath = self.transcripts_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)

        print(f"✅ Транскрипт сохранен: {filepath}")
        return filepath

    def load_local_transcript(self, filepath: str) -> Dict:
        """
        Загрузить транскрипт из локального файла

        Args:
            filepath: Путь к файлу транскрипта

        Returns:
            Данные транскрипта
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _matches_project_filters(self, transcript: Dict) -> bool:
        """
        Проверяет, соответствует ли транскрипт фильтрам проекта

        Args:
            transcript: Данные транскрипта

        Returns:
            True если транскрипт относится к проекту
        """
        team_members = self.config.get("team_members", [])
        keywords = self.config.get("keywords", [])

        # Проверяем участников
        participants = transcript.get("participants", [])
        organizer = transcript.get("organizer_email", "")

        # Если есть фильтр по участникам, проверяем пересечение
        if team_members:
            all_people = participants + ([organizer] if organizer else [])
            # Проверяем, есть ли хотя бы один участник из команды
            has_team_member = any(
                any(member.lower() in person.lower() for member in team_members)
                for person in all_people
            )
            if not has_team_member:
                return False

        # Дополнительная проверка по ключевым словам в названии (опционально)
        if keywords:
            title = transcript.get("title", "").lower()
            has_keyword = any(kw.lower() in title for kw in keywords)
            # Если есть ключевое слово - точно подходит
            if has_keyword:
                return True

        # Если прошли фильтр участников или нет фильтров - подходит
        return True if team_members else False

    def filter_project_transcripts(self, transcripts: List[Dict]) -> List[Dict]:
        """
        Фильтрует транскрипты, оставляя только относящиеся к проекту

        Args:
            transcripts: Список всех транскриптов

        Returns:
            Отфильтрованный список транскриптов
        """
        filtered = [t for t in transcripts if self._matches_project_filters(t)]

        print(f"📊 Из {len(transcripts)} транскриптов найдено {len(filtered)} по проекту {self.config.get('project_name', 'healthy4u')}")

        return filtered

    def sync_transcripts(self, limit: int = 10, filter_by_project: bool = True) -> List[Path]:
        """
        Синхронизировать последние транскрипты с Fireflies

        Args:
            limit: Количество последних транскриптов для синхронизации
            filter_by_project: Фильтровать только транскрипты проекта (по умолчанию True)

        Returns:
            Список путей к сохраненным файлам
        """
        print(f"🔄 Синхронизация последних {limit} транскриптов...")

        try:
            transcripts = self.get_recent_transcripts(limit)

            # Фильтруем по проекту если нужно
            if filter_by_project:
                transcripts = self.filter_project_transcripts(transcripts)

            saved_files = []

            for transcript in transcripts:
                filepath = self.save_transcript(transcript)
                saved_files.append(filepath)

            print(f"✅ Синхронизировано {len(saved_files)} транскриптов")
            return saved_files

        except Exception as e:
            print(f"❌ Ошибка синхронизации: {e}")
            return []


def main():
    """Основная функция для тестирования клиента"""
    client = FirefliesClient()

    if not client.api_key:
        print("\n📋 Инструкция по получению API ключа:")
        print("1. Войдите в https://app.fireflies.ai")
        print("2. Перейдите в Settings → Integrations → API")
        print("3. Создайте новый API ключ")
        print("4. Установите переменную окружения: export FIREFLIES_API_KEY='ваш_ключ'")
        print("   Или создайте файл .env с содержимым: FIREFLIES_API_KEY=ваш_ключ")
        return

    # Синхронизация последних транскриптов
    client.sync_transcripts(limit=5)


if __name__ == "__main__":
    main()
