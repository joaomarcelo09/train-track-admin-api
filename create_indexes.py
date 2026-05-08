"""
MongoDB Index Setup Script
Run this script to create optimal indexes for the application.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database.connection import connect_to_mongo, close_mongo_connection, get_database

async def create_indexes():
    await connect_to_mongo()
    db = get_database()

    # Line collection indexes
    await db.lines.create_index("name", unique=True)
    await db.lines.create_index("id")

    # Train collection indexes
    await db.trains.create_index("id")

    # Track collection indexes
    await db.tracks.create_index("id")
    await db.tracks.create_index("id_line")
    await db.tracks.create_index("elevation")
    await db.tracks.create_index("bending")
    await db.tracks.create_index("length")

    # User collection indexes
    await db.users.create_index("id")
    await db.users.create_index("email", unique=True)

    print("Indexes created successfully")

    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(create_indexes())