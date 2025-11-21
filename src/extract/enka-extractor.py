# src/extract/enka_extractor.py
import asyncio
import json
from pathlib import Path
from enka import HSRClient

async def fetch_user_data(uid: int):
    """
    Extract player info, characters, and builds from HSR showcase.
    Saves raw JSON for ETL practice.
    """
    async with HSRClient() as client:
        data = await client.fetch_showcase(uid)

        # ---------- PLAYER INFO ----------
        player_info = {
            "uid": uid,
            "nickname": data.player.nickname,
            "level": data.player.level,
            "signature": data.player.signature,
        }

        # ---------- CHARACTERS INFO ----------
        characters = []
        builds = []

        for char in data.characters:
            char_dict = {
                "character_id": char.id,
                "name": char.name,
                "level": char.level,
                #"promotion": char.promotion,
                "element": char.element,
            }
            characters.append(char_dict)

            # Build = light cone + relics
            build_dict = {
                "character_id": char.id,
                "character_name": char.name,
                "light_cone": char.light_cone.name if getattr(char, "light_cone", None) else None,
                "light_cone_level": char.light_cone.level if getattr(char, "light_cone", None) else None,
            }
            builds.append(build_dict)

        # ---------- SAVE RAW JSON ----------
        raw_path = Path("data/raw")
        raw_path.mkdir(parents=True, exist_ok=True)

        filename = raw_path / f"hsr_{uid}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "player": player_info,
                "characters": characters,
                "builds": builds
            }, f, indent=2, ensure_ascii=False)

        print(f"✅ Raw data saved to {filename}")

        # ---------- PRINT INFO ----------
        print("\n=== Player Info ===")
        for k, v in player_info.items():
            print(f"{k}: {v}")

        print("\n=== Characters ===")
        for char in characters:
            print(f"{char['name']} | Level: {char['level']} | Element: {char['element']}")

        print("\n=== Builds ===")
        for build in builds:
            print(f"Build for {build['character_name']}:")
            print(f"  Light Cone: {build['light_cone']} (Level {build['light_cone_level']})")
            print("---")


if __name__ == "__main__":
    uid = 700712292
    asyncio.run(fetch_user_data(uid))
