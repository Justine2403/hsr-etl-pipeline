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
            #"signature": data.player.signature,
        }

        # ---------- CHARACTERS + BUILDS + RELICS ----------
        characters = []
        builds = []
        stats_data = []
        relics_data = []

        for char in data.characters:
            # Character info
            char_dict = {
                "character_id": char.id,
                "name": char.name,
                "level": char.level,
                "element": char.element,
            }
            characters.append(char_dict)

            # Build info (light cone)
            build_dict = {
                "character_id": char.id,
                "character_name": char.name,
                "light_cone": char.light_cone.name if getattr(char, "light_cone", None) else None,
                "light_cone_level": char.light_cone.level if getattr(char, "light_cone", None) else None,
            }
            builds.append(build_dict)

            # ---------- STATS ----------
            if getattr(char, "stats", None):
                stats_dict = {"character_id": char.id, "character_name": char.name,  }
                
                # Fetch all stats dynamically, same style as relics
                for stat_key, stat_obj in char.stats.items():
                    stats_dict[stat_obj.name] = stat_obj.value

                stats_data.append(stats_dict)

            # ---------- RELICS ----------
            for relic in getattr(char, "relics", []):
                relic_dict = {
                    "character_name": char.name,
                    "relic_id": relic.id,
                    "slot": relic.type.name,
                    "set_name": relic.set_name,
                    "set_id": relic.set_id,
                    "rarity": relic.rarity,
                    "main_stat_name": relic.main_stat.name if relic.main_stat else None,
                    "main_stat_value": relic.main_stat.value if relic.main_stat else None,
                    "main_stat_is_percent": relic.main_stat.is_percentage if relic.main_stat else None,
                    "icon": relic.icon,
                }

                # Flatten substats
                for i, sub in enumerate(getattr(relic, "sub_stats", []), start=1):
                    relic_dict[f"substat{i}_name"] = sub.name
                    relic_dict[f"substat{i}_value"] = sub.value
                    relic_dict[f"substat{i}_is_percent"] = sub.is_percentage

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
                "builds": builds,
                "relics": relics_data
            }, f, indent=2, ensure_ascii=False)

        print(f"Raw data saved to {filename}")


        # ---------- PRINT INFO ----------
        for char, build in zip(characters, builds):
            print(f"\nCharacter: {char['name']} | Level {char['level']} | Element: {char['element']}")
           
            # Main stats

            print("\nStats: ")
            char_stats = next((s for s in stats_data if s['character_name'] == char['name']), {})
            if char_stats:
                stat_lines = [f"{k}: {v}" for k, v in char_stats.items() if k != "character_name"]
                print(" | ".join(stat_lines))

            print(f"\nLight Cone: {build['light_cone']} (Level {build['light_cone_level']})")
        
            # Relics for this character
            char_relics = [r for r in relics_data if r['character_name'] == char['name']]
            print("\nRelics: ")
            for relic in char_relics:
                print(f"  [{relic['slot']}] {relic['set_name']} (Rarity: {relic['rarity']})")
                print(f"    Main: {relic['main_stat_name']} = {relic['main_stat_value']}")
                substats = []
                for i in range(1, 6):
                    if f"substat{i}_name" in relic:
                        substats.append(f"{relic[f'substat{i}_name']} = {relic[f'substat{i}_value']}")
                if substats:
                    print("    Substats: " + " | ".join(substats))
                print("\n")
            print("-"*50)

if __name__ == "__main__":
    uid = 700712292
    asyncio.run(fetch_user_data(uid))