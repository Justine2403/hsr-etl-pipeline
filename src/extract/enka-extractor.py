# src/extract/enka_extractor.py
import asyncio
import json
from pathlib import Path
from enka import HSRClient

async def fetch_user_data(uid: int):
    async with HSRClient() as client:
        data = await client.fetch_showcase(uid)

        # ---------- PLAYER INFO ----------
        player_info = {
            "uid": uid,
            "nickname": data.player.nickname,
            "level": data.player.level,
        }

        # ---------- CHARACTERS, STATS, AND RELICS ----------
        characters = []
        stats_data = []
        relics_data = []

        for char in data.characters:
            # Character info
            char_dict = {
                "character_id": char.id,
                "name": char.name,
                "level": char.level,
                "element": char.element,
                "light_cone": getattr(char.light_cone, "name", None),
                "light_cone_level": getattr(char.light_cone, "level", None)
            }
            characters.append(char_dict)

            # Character stats
            if getattr(char, "stats", None):
                stats_dict = {"character_id": char.id, "character_name": char.name,  }
                
                # Fetch all stats dynamically
                # Slice dictionnary to get only 6 first stats
                for stat_key, stat_obj in list(char.stats.items())[:6]:
                    for _ in range(5):
                        stats_dict[stat_obj.name] = stat_obj.value

                stats_data.append(stats_dict)

            # Character relics
            for relic in getattr(char, "relics", []):
                relic_dict = {
                    "character_name": char.name,
                    "relic_id": relic.id,
                    "slot": relic.type.name,
                    "set_name": relic.set_name,
                    "set_id": relic.set_id,
                    "rarity": relic.rarity,
                    "main_stat_name": getattr(relic.main_stat, "name", None),
                    "main_stat_value": getattr(relic.main_stat, "value", None),
                    "main_stat_is_percent": getattr(relic.main_stat, "is_percentage", None),
                    "icon": relic.icon,
                    "substats": [
                        {
                            "name": s.name,
                            "value": s.value,
                            "is_percent": s.is_percentage
                        }
                        for s in getattr(relic, "sub_stats", [])
                    ]
                }
                relics_data.append(relic_dict)

        # ---------- SAVE RAW JSON ----------
        raw_path = Path("data/raw")
        raw_path.mkdir(parents=True, exist_ok=True)
        filename = raw_path / f"hsr_{uid}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "player": player_info,
                "characters": characters,
                "stats": stats_data,
                "relics": relics_data
            }, f, indent=2, ensure_ascii=False)

        print(f"Raw data saved to {filename}")

        # ---------- PRINT INFO ----------
        for char in characters:
            print(f"\nCharacter: {char['name']} | Level {char['level']} | Element: {char['element']}")
            print(f"Lightcone: {char['light_cone']} | Level {char['light_cone_level']}")

            # Stats
            char_stats = next((s for s in stats_data if s['character_name'] == char['name']), {})
            if char_stats:
                stat_lines = [f"{k}: {v}" for k, v in char_stats.items() if k != "character_name"]
                print("Stats: " + " | ".join(stat_lines))

            # Relics
            char_relics = [r for r in relics_data if r['character_name'] == char['name']]
            if char_relics:
                print("Relics:")
                for relic in char_relics:
                    print(f"  [{relic['slot']}] {relic['set_name']} (Rarity: {relic['rarity']})")
                    print(f"    Main: {relic['main_stat_name']} = {relic['main_stat_value']}")
                    if relic['substats']:
                        substats_lines = [f"{s['name']} = {s['value']}" for s in relic['substats']]
                        print("    Substats: " + " | ".join(substats_lines))
            print("-" * 50)

if __name__ == "__main__":
    import sys
    uid = int(sys.argv[1])  # pass UID as argument
    asyncio.run(fetch_user_data(uid))
