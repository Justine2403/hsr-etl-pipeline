import streamlit as st
import json
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

st.set_page_config(page_title="HSR Analyzer", layout="wide")
st.title("⭐ Honkai Star Rail – Profile Viewer")

# USER INPUT
available_uids = [
    p.stem.replace("hsr_", "") 
    for p in RAW_DIR.glob("hsr_*.json")
]

uid = st.selectbox("Select a UID", available_uids)

if uid:
    raw_path = RAW_DIR / f"hsr_{uid}.json"
    char_csv = PROCESSED_DIR / f"characters_{uid}.csv"
    relic_csv = PROCESSED_DIR / f"relics_{uid}.csv"

    if not raw_path.exists():
        st.error("No data found. Please run extraction first.")
        st.stop()

    # LOAD DATA
    with open(raw_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    chars_df = pd.read_csv(char_csv)
    relics_df = pd.read_csv(relic_csv)

    # PLAYER INFO
    st.header("Player Info")
    player = raw["player"]
    col1, col2, col3 = st.columns(3)
    col1.metric("UID", player["uid"])
    col2.metric("Nickname", player["nickname"])
    col3.metric("Account Level", player["level"])
    st.divider()

    # CHARACTER INFO
    st.header("Characters")
    for char_name in chars_df["character_name"].unique():
        char_data = chars_df[chars_df["character_name"] == char_name].iloc[0]

        with st.expander(f"{char_data['character_name']} — Lv. {char_data['character_level']}"):

            # Character base info
            st.subheader("Character Info")
            c1, c2, c3, c4 = st.columns(4)
            c1.write(f"**Element**: {char_data['element']}")
            c2.write(f"**Light Cone**: {char_data['light_cone']}")
            c3.write(f"**LC Level**: {char_data['light_cone_level']}")
            c4.write(f"**Character ID**: {char_data['character_id']}")

            # Stats
            st.subheader("Stats")
            stats_cols = st.columns(6)
            stats_cols[0].metric("HP", char_data["HP"])
            stats_cols[1].metric("ATK", char_data["ATK"])
            stats_cols[2].metric("DEF", char_data["DEF"])
            stats_cols[3].metric("SPD", char_data["SPD"])
            stats_cols[4].metric("CRIT Rate %", char_data["CRIT Rate"])
            stats_cols[5].metric("CRIT DMG %", char_data["CRIT DMG"])

            st.divider()

            # RELICS FOR THIS CHARACTER
            st.subheader("Relics")
            char_relics = [r for r in raw.get("relics", []) if r["character_name"] == char_name]

            for relic in char_relics:
                with st.container():
                    st.markdown(f"### {relic['slot']} — ⭐{relic['rarity']} {relic['set_name']}")

                    # Display relic icon if exists
                    if relic.get("icon"):
                        st.image(relic["icon"], width=60)

                    main_value = relic['main_stat_value']
                    if relic.get('main_stat_is_percent'):
                        main_value = round(main_value, 2)
                    else:
                        main_value = int(main_value)

                    st.write(f"**Main Stat**: {relic['main_stat_name']} = {main_value}")
                    # Substats (all)
                    if relic.get("substats"):
                        for sub in relic["substats"]:
                            val = sub["value"]
                            if sub.get("is_percent"):
                                val = round(val, 2)
                            else:
                                val = int(val)
                            st.write(f"**Substat**: {sub['name']} = {val}")

                    st.divider()
