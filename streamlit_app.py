# File Name team_roster_app.py
# Description: A simple Streamlit app to create a team roster based on list of players and skill level inputted. 

import streamlit as st
import random

st.title("🏆 Team Roster Generator")
st.write("Paste your list of player names and assign skill levels to generate balanced teams.")

# Input section
player_input = st.text_area("Paste player names (one per line):", height=200)

skill_levels = ["Beginner", "Intermediate", "Advanced"]
default_level = "Intermediate"

# Skill assignment
players = [name.strip() for name in player_input.split("\n") if name.strip()]
player_data = []

if players:
    st.subheader("Assign Skill Levels")
    for name in players:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.text(name)
        with col2:
            level = st.selectbox(f"Skill level for {name}", skill_levels, index=1, key=name)
            player_data.append((name, level))

# Team generation logic
def create_balanced_teams(player_list, team_min=10, team_max=12):
    groups = {'Beginner': [], 'Intermediate': [], 'Advanced': []}
    for name, level in player_list:
        groups[level].append(name)

    for key in groups:
        random.shuffle(groups[key])

    total_players = len(player_list)
    if total_players < team_min:
        return []

    avg_size = (team_min + team_max) // 2
    nteams = max(1, total_players // avg_size)
    if total_players % nteams > team_max:
        nteams += 1

    teams = [[] for _ in range(nteams)]

    for level, players in groups.items():
        for idx, player in enumerate(players):
            teams[idx % nteams].append((player, level))

    changed = True
    while changed:
        changed = False
        team_sizes = [len(team) for team in teams]
        for i in range(nteams):
            if team_sizes[i] > team_max:
                for j in range(nteams):
                    if team_sizes[j] < team_min:
                        player_to_move = teams[i].pop()
                        teams[j].append(player_to_move)
                        changed = True
                        break
    return teams

# Generate teams
if st.button("Generate Teams"):
    if len(player_data) < 10:
        st.warning("You need at least 10 players to form a team.")
    else:
        teams = create_balanced_teams(player_data)
        st.success(f"{len(teams)} teams generated!")
        for idx, team in enumerate(teams):
            st.subheader(f"Team {idx + 1} ({len(team)} players)")
            for player, level in team:
                st.write(f"- {player} ({level})")
