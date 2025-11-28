# src/transform/transform.py
import json
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def transform_user(uid: int):
    # ---------- Load raw JSON ----------
    raw_file = RAW_DIR / f"hsr_{uid}.json"
    with open(raw_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ---------- Transform Characters ----------
    chars = []
    for char in data.get("characters", []):
        char_stats = next((s for s in data.get("stats", []) if s["character_name"] == char["name"]), {})
        chars.append({
            "uid": data["player"]["uid"],
            "nickname": data["player"]["nickname"],
            "level": data["player"]["level"],
            "character_id": char["character_id"],
            "character_name": char["name"],
            "character_level": char["level"],
            "element": char["element"],
            "light_cone": char["light_cone"],
            "light_cone_level": char["light_cone_level"],
            "HP": int(char_stats.get("HP")),
            "ATK": int(char_stats.get("ATK")),
            "DEF": int(char_stats.get("DEF")),
            "SPD": int(char_stats.get("SPD")),
            "CRIT Rate": round(char_stats.get("CRIT Rate"), 2),
            "CRIT DMG": round(char_stats.get("CRIT DMG"),2)
        })

    # ---------- Transform Relics ----------
    relics = []
    for relic in data.get("relics", []):
        substats = relic.get("substats", [])
        
        main_value = relic["main_stat_value"]
        if relic["main_stat_is_percent"]:
            main_value = round(main_value * 100, 2)
        else:
            main_value = int(main_value)

        formatted_substats = []
        for sub in substats[:4]:
            val = sub["value"]
            if sub.get("is_percent"):
                val = round(val * 100, 2)
            elif val is not None:
                val = int(val)
            formatted_substats.append({
                "name": sub["name"],
                "value": val,
                "is_percent": sub["is_percent"]
            })

        while len(formatted_substats) < 4:
            formatted_substats.append({"name": None, "value": None, "is_percent": None})

        relics.append({
            "uid": data["player"]["uid"],
            "character_name": relic["character_name"],
            "slot": relic["slot"],
            "set_name": relic["set_name"],
            "rarity": relic["rarity"],
            "main_stat_name": relic["main_stat_name"],
            "main_stat_value": main_value,
            "main_stat_is_percent": relic["main_stat_is_percent"],
            "substats": formatted_substats,
            "num_substats": len(substats)
        })


    # ---------- Save CSV ----------
    chars_df = pd.DataFrame(chars)
    chars_df.to_csv(PROCESSED_DIR / f"characters_{uid}.csv", index=False, encoding="utf-8")
    print(f"Processed character data saved to {PROCESSED_DIR / f'characters_{uid}.csv'}")

    relics_df = pd.DataFrame(relics)
    relics_df.to_csv(PROCESSED_DIR / f"relics_{uid}.csv", index=False, encoding="utf-8")
    print(f"Processed relics data saved to {PROCESSED_DIR / f'relics_{uid}.csv'}")


if __name__ == "__main__":
    import sys
    uid = int(sys.argv[1])
    transform_user(uid)