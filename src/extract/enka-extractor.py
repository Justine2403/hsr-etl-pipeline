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

        # ---------- CHARACTERS + BUILDS ----------
        characters = []
        stats_data = []
        relics_data = []

        for char in data.characters:
            # Character info and lightcone
            char_dict = {
                "character_id": char.id,
                "name": char.name,
                "level": char.level,
                "element": char.element,
                "light_cone": char.light_cone.name if getattr(char, "light_cone", None) else None,
                "light_cone_level": char.light_cone.level if getattr(char, "light_cone", None) else None
            }
            characters.append(char_dict)

           
            # ---------- STATS ----------
            if getattr(char, "stats", None):
                stats_dict = {"character_id": char.id, "character_name": char.name,  }
                
                # Fetch all stats dynamically
                # Slice dictionnary to get only 6 first stats
                for stat_key, stat_obj in list(char.stats.items())[:6]:
                    for _ in range(5):
                        stats_dict[stat_obj.name] = stat_obj.value

                stats_data.append(stats_dict)

            # ---------- BUILD/RELICS ----------
            if getattr(char, "relics", None):
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
                "relics": relics_data
            }, f, indent=2, ensure_ascii=False)

        print(f"Raw data saved to {filename}")

        # ---------- PRINT INFO TO CHECK ----------
        for char in characters:
            print(f"\nCharacter: {char['name']} | Level {char['level']} | Element: {char['element']}")
            print(f"\nLightcone: {char['light_cone']} | Level {char['light_cone_level']}")

            # Main stats

            print("\nStats: ")
            char_stats = next((s for s in stats_data if s['character_name'] == char['name']), {})
            if char_stats:
                stat_lines = [f"{k}: {v}" for k, v in char_stats.items() if k != "character_name"]
                print(" | ".join(stat_lines))
        
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
                    print("Substats: " + " | ".join(substats))
                print("\n")
            print("-"*50)

if __name__ == "__main__":
    uid = 700712292
    uid_test = 721686624
    asyncio.run(fetch_user_data(uid_test))
