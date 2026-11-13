
import json
from pathlib import Path

from storage.account_storage import get_account_storage_directory


class LearningProgressManager:

    def __init__(self, username=None):

        if username:
            account_directory = get_account_storage_directory(username)
            self.file_path = account_directory / "learning_progress.json"
        else:
            self.file_path = (
                Path(__file__).resolve().parent
                / "learning_progress.json"
            )

    def load_progress(
        self,
        lesson_count=4,
        challenge_count=5
    ):

        default_progress = {
            "completed_lessons": [],
            "completed_challenges": [],
            "challenge_xp": 0
        }

        if not self.file_path.exists():
            return default_progress

        try:

            data = json.loads(
                self.file_path.read_text(encoding="utf-8")
            )

            if not isinstance(data, dict):
                return default_progress

            lessons = data.get("completed_lessons", [])
            challenges = data.get("completed_challenges", [])

            if not isinstance(lessons, list):
                lessons = []

            if not isinstance(challenges, list):
                challenges = []

            completed_lessons = {
                item for item in lessons
                if isinstance(item, int)
                and not isinstance(item, bool)
                and 0 <= item < lesson_count
            }

            completed_challenges = {
                item for item in challenges
                if isinstance(item, int)
                and not isinstance(item, bool)
                and 0 <= item < challenge_count
            }

            challenge_xp = data.get("challenge_xp", 0)

            if (
                not isinstance(challenge_xp, int)
                or isinstance(challenge_xp, bool)
                or challenge_xp < 0
            ):
                challenge_xp = 0

            return {
                "completed_lessons": sorted(completed_lessons),
                "completed_challenges": sorted(completed_challenges),
                "challenge_xp": challenge_xp
            }

        except (OSError, json.JSONDecodeError, TypeError):
            return default_progress

    def save_progress(
        self,
        completed_lessons,
        completed_challenges,
        challenge_xp=0
    ):

        data = {
            "completed_lessons": sorted(
                int(item) for item in completed_lessons
            ),
            "completed_challenges": sorted(
                int(item) for item in completed_challenges
            ),
            "challenge_xp": max(0, int(challenge_xp))
        }

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        temporary_path = self.file_path.with_suffix(".tmp")

        temporary_path.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        temporary_path.replace(self.file_path)
