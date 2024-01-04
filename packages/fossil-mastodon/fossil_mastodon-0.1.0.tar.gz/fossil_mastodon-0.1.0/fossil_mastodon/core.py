import datetime
import functools
import json
import logging
import sqlite3
from typing import Optional
import html2text
import llm
import numpy as np

import requests

from fossil_mastodon import config
import os
from pydantic import BaseModel

logger = logging.getLogger(__name__)


@functools.cache
def create_database():
    if os.path.exists(config.DATABASE_PATH):
        return

    print("Creating database")
    with sqlite3.connect(config.DATABASE_PATH) as conn:
        c = conn.cursor()

        # Create the toots table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS toots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                author TEXT,
                url TEXT,
                created_at DATETIME,
                embedding BLOB,
                orig_json TEXT,
                cluster TEXT  -- Added cluster column
            )
        ''')

        conn.commit()


@functools.lru_cache()
def _get_json(toot: "Toot") -> dict:
    # meh, this isn't great, but it works
    import json
    return json.loads(toot.orig_json)


class MediaAttatchment(BaseModel):
    type: str
    preview_url: str
    url: str


class Toot(BaseModel):
    class Config:
        arbitrary_types_allowed = True
    id: int | None = None
    content: str | None
    author: str | None
    url: str | None
    created_at: datetime.datetime
    embedding: np.ndarray | None = None
    orig_json: str | None = None
    cluster: str | None = None  # Added cluster property

    @property
    def orig_dict(self) -> dict:
        return _get_json(self)

    @property
    def avatar_url(self) -> str | None:
        return self.orig_dict.get("account", {}).get("avatar")
    
    @property
    def profile_url(self) -> str | None:    
        return self.orig_dict.get("account", {}).get("url")

    @property
    def display_name(self) -> str | None:
        return self.orig_dict.get("account", {}).get("display_name")

    @property
    def toot_id(self) -> str | None:
        return self.orig_dict.get("id")

    @property
    def is_reply(self) -> bool:
        return self.orig_dict.get("in_reply_to_id") is not None

    @property
    def media_attachments(self) -> list[MediaAttatchment]:
        return [MediaAttatchment(type=m.get("type"), url=m.get("url"), preview_url=m.get("preview_url")) 
                for m in self.orig_dict.get("media_attachments", [])]

    @property
    def card_preview_url(self) -> str | None:
        return self.orig_dict.get("card", {}).get("image")

    @property
    def card_url(self) -> str | None:
        return self.orig_dict.get("card", {}).get("url")

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url

    def save(self, init_conn: sqlite3.Connection | None = None) -> bool:
        try:
            if init_conn is None:
                conn = sqlite3.connect(config.DATABASE_PATH)
            else:
                conn = init_conn
            create_database()
            c = conn.cursor()

            # Check if the URL already exists
            c.execute('''
                SELECT COUNT(*) FROM toots WHERE url = ? and embedding is not null
            ''', (self.url,))

            result = c.fetchone()
            url_exists = result[0] > 0

            if url_exists:
                # URL already exists, handle accordingly
                return False

            c.execute('''
                DELETE FROM toots WHERE url = ?
            ''', (self.url,))

            embedding = self.embedding.tobytes() if self.embedding is not None else bytes()
            c.execute('''
                INSERT INTO toots (content, author, url, created_at, embedding, orig_json, cluster)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.content, self.author, self.url, self.created_at, embedding, self.orig_json, self.cluster))

        except:
            conn.rollback()
            raise
        finally:
            if init_conn is None:
                conn.commit()
        return True

    @classmethod
    def get_toots_since(cls, since: datetime.datetime) -> list["Toot"]:
        create_database()
        with sqlite3.connect(config.DATABASE_PATH) as conn:
            c = conn.cursor()

            c.execute('''
                SELECT 
                    id, content, author, url, created_at, embedding, orig_json, cluster
                FROM toots WHERE created_at >= ?
            ''', (since,))

            rows = c.fetchall()
            toots = []
            for row in rows:
                toot = cls(
                    id=row[0],
                    content=row[1],
                    author=row[2],
                    url=row[3],
                    created_at=row[4],
                    embedding=np.frombuffer(row[5]) if row[5] else None,
                    orig_json=row[6],
                    cluster=row[7]  # Added cluster property
                )
                toots.append(toot)

            return toots

    @classmethod
    def get_by_id(cls, id: int) -> Optional["Toot"]:
        create_database()
        with sqlite3.connect(config.DATABASE_PATH) as conn:
            c = conn.cursor()

            c.execute('''
                SELECT 
                    id, content, author, url, created_at, embedding, orig_json, cluster
                FROM toots WHERE id = ?
            ''', (id,))

            row = c.fetchone()
            if row:
                toot = cls(
                    id=row[0],
                    content=row[1],
                    author=row[2],
                    url=row[3],
                    created_at=row[4],
                    embedding=np.frombuffer(row[5]) if row[5] else None,
                    orig_json=row[6],
                    cluster=row[7],  # Added cluster property
                )
                return toot
            return None

    @staticmethod
    def get_latest_date() -> datetime.datetime | None:
        create_database()
        with sqlite3.connect(config.DATABASE_PATH) as conn:
            c = conn.cursor()

            c.execute('''
                SELECT MAX(created_at) FROM toots
            ''')

            result = c.fetchone()
            latest_date = result[0] if result[0] else None

            if isinstance(latest_date, str):
                try:
                    latest_date = datetime.datetime.strptime(latest_date, "%Y-%m-%d %H:%M:%S.%f")
                except ValueError:
                    latest_date = datetime.datetime.strptime(latest_date, "%Y-%m-%d %H:%M:%S")
            return latest_date

    @classmethod
    def from_dict(cls, data):
        import json

        if data.get("reblog"):
            return cls.from_dict(data["reblog"])

        return cls(
            content=data.get("content"),
            author=data.get("account", {}).get("acct"),
            url=data.get("url"),
            created_at=datetime.datetime.strptime(data.get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ"),
            orig_json=json.dumps(data),
        )

    def do_star(self):
        print("star", self.url)

    def do_boost(self):
        print("boost", self.url)


def get_toots_since(since: datetime.datetime):
    assert isinstance(since, datetime.datetime), type(since)
    create_database()
    download_timeline(since)
    return Toot.get_toots_since(since)


def download_timeline(since: datetime.datetime):
    last_date = Toot.get_latest_date()
    logger.info(f"last toot date: {last_date}")
    last_date = last_date or since
    earliest_date = None
    buffer: list[Toot] = []
    last_id = ""
    curr_url = f"{config.MASTO_BASE}/api/v1/timelines/home?limit=40"
    import json as JSON
    while not earliest_date or earliest_date > last_date:
        response = requests.get(curr_url, headers=config.headers())
        response.raise_for_status()
        json = response.json()
        if not json:
            logger.info("No more toots")
            break
        if len(json) > 1:
            last_id = json[-1]["id"]
        logger.info(f"Got {len(json)} toots; earliest={earliest_date.isoformat() if earliest_date else None}, last_id={last_id}")
        for toot_dict in json:
            toot = Toot.from_dict(toot_dict)
            earliest_date = toot.created_at if not earliest_date else min(earliest_date, datetime.datetime.strptime(toot_dict["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"))
            buffer.append(toot)

        if "next" in response.links:
            curr_url = response.links["next"]["url"]
        else:
            break
    logger.info(f"done with toots; earliest={earliest_date.isoformat() if earliest_date else None}, last_date: {last_date.isoformat() if last_date else None}")

    # Set embeddings in batches of 100
    page_size = 50
    num_pages = len(buffer) // page_size
    for page in range(num_pages):
        start_index = page * page_size
        end_index = start_index + page_size
        page_toots = buffer[start_index:end_index]

        # Example: Call the _create_embeddings function
        _create_embeddings(page_toots)
        with sqlite3.connect(config.DATABASE_PATH) as conn:
            for toot in page_toots:
                toot.save(init_conn=conn)


def _create_embeddings(toots: list[Toot]):
    # Convert the list of toots to a single string
    toots = [t for t in toots if t.content]

    # Call the llm embedding API to create embeddings
    emb_model = llm.get_embedding_model(config.EMBEDDING_MODEL.name)
    embeddings = list(emb_model.embed_batch([html2text.html2text(t.content) for t in toots]))

    # Extract the embeddings from the API response
    print(f"got {len(embeddings)} embeddings")
    for i, toot in enumerate(toots):
        toot.embedding = np.array(embeddings[i])

    # Return the embeddings
    return toots


@functools.lru_cache()
def _create_session_table():
    create_database()
    with sqlite3.connect(config.DATABASE_PATH) as conn:
        c = conn.cursor()

        # Create the toots table if it doesn't exist
        c.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                algorithm_spec TEXT,
                algorithm BLOB,
                ui_settings TEXT
            )
        ''')

        conn.commit()


class Session(BaseModel):
    id: str
    algorithm_spec: str | None = None
    algorithm: bytes | None = None
    ui_settings: str | None = None

    def set_ui_settings(self, ui_settings: dict[str, str]):
        self.ui_settings = json.dumps(ui_settings)
        self.save()

    def get_ui_settings(self) -> dict[str, str]:
        return json.loads(self.ui_settings or "{}")

    @classmethod
    def get_by_id(cls, id: str) -> Optional["Session"]:
        create_database()
        _create_session_table()
        with sqlite3.connect(config.DATABASE_PATH) as conn:
            c = conn.cursor()

            c.execute('''
                SELECT id, algorithm_spec, algorithm, ui_settings FROM sessions WHERE id = ?
            ''', (id,))

            row = c.fetchone()
            if row:
                session = cls(
                    id=row[0],
                    algorithm_spec=row[1],
                    algorithm=row[2],
                    ui_settings=row[3],
                )
                return session
            return None

    @classmethod
    def create(cls) -> "Session":
        import uuid
        return cls(id=str(uuid.uuid4()).replace("-", ""))

    def save(self, init_conn: sqlite3.Connection | None = None) -> bool:
        _create_session_table()
        try:
            if init_conn is None:
                conn = sqlite3.connect(config.DATABASE_PATH)
            else:
                conn = init_conn
            create_database()
            c = conn.cursor()

            c.execute('''
                INSERT INTO sessions (id, algorithm_spec, algorithm, ui_settings)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE 
                    SET algorithm_spec = excluded.algorithm_spec
                      , algorithm = excluded.algorithm
                      , ui_settings = excluded.ui_settings
            ''', (self.id, self.algorithm_spec, self.algorithm, self.ui_settings))

            if init_conn is None:
                conn.commit()
        except:
            conn.rollback()
            raise
        return True
