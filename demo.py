import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

'# Project: NBA Database'


@st.cache
def get_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f'Running query_db(): {sql}')

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df


'## Read tables'

sql_all_table_names = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
all_table_names = query_db(sql_all_table_names)['relname'].tolist()
table_name = st.selectbox('Choose a table', all_table_names)
if table_name:
    f'Display the table'

    sql_table = f'select * from {table_name};'
    df = query_db(sql_table)
    st.dataframe(df)

# codes for NBA project

'## Teams Infomation'
display_type = st.radio("Display teams by: ", ("Conferences", "Divisions"))

if display_type:
    if display_type == "Conferences":
        sql_conferences = "SELECT DISTINCT(conference) FROM Teams;"
        conferences = query_db(sql_conferences)['conference'].tolist()
        selected_conference = st.radio("Choose a conference", conferences)
        sql_teams = (
                        "SELECT TM.Team, TM.City, TM.Arena, TM.Coach, TM.Owner, Count(S.year) as Champions FROM ( "
                            "SELECT T.team_id as ID, T.name as Team, T.arena_city as City, T.arena_name as Arena, C.name as Coach, O.name as Owner "
                            "FROM Teams T, Coaches C, Owners O "
                            "WHERE T.team_id = O.team_id "
                            "AND T.team_id = C.team_id "
                            f"AND T.conference = '{selected_conference}' "
                        ") as TM "
                        "LEFT JOIN Seasons as S "
                        "ON S.champion_team_id = TM.ID "
                        "GROUP BY TM.Team, TM.City, TM.Arena, TM.Coach, TM.Owner;"
        )
        teams = query_db(sql_teams)
        st.dataframe(teams)
    elif display_type == "Divisions":
        sql_divisions = "SELECT DISTINCT(division) FROM Teams;"
        divisions = query_db(sql_divisions)['division'].tolist()
        selected_division = st.selectbox("Choose a division", divisions)
        sql_teams = (
                        "SELECT TM.Team, TM.City, TM.Arena, TM.Coach, TM.Owner, Count(S.year) as Champions FROM ( "
                            "SELECT T.team_id as ID, T.name as Team, T.arena_city as City, T.arena_name as Arena, C.name as Coach, O.name as Owner "
                            "FROM Teams T, Coaches C, Owners O "
                            "WHERE T.team_id = O.team_id "
                            "AND T.team_id = C.team_id "
                            f"AND T.division = '{selected_division}' "
                        ") as TM "
                        "LEFT JOIN Seasons as S "
                        "ON S.champion_team_id = TM.ID "
                        "GROUP BY TM.Team, TM.City, TM.Arena, TM.Coach, TM.Owner;"
        )
        teams = query_db(sql_teams)
        st.dataframe(teams)

'## Season Summary'

sql_seasons = 'SELECT DISTINCT(year) from Seasons ORDER BY year;'
seasons = query_db(sql_seasons)['year'].tolist()
selected_season = st.selectbox('Choose a season', seasons)

if selected_season:
    sql_awards = (
                    "SELECT A.name as Award, P.name as Player "
                    "FROM Players P, Player_Wins_Award PWA, Awards A "
                    f"WHERE PWA.season = {selected_season} "
                    "AND PWA.award = A.name "
                    "AND PWA.player_id = P.player_id;"
    )

    sql_champion = (
                        "SELECT T.name as Team, T.arena_city as City "
                        "FROM Teams T, Seasons S "
                        f"WHERE S.year = {selected_season} " 
                        "AND S.champion_team_id = T.team_id;"
    )
    
    sql_points_leaders = (
                            "SELECT P.name as Player, PSP.avg_points as Points "
                            "FROM Players P, Player_Season_Performance PSP "
                            f"WHERE PSP.season = {selected_season} "
                            "AND PSP.player_id = P.player_id "
                            "ORDER BY PSP.avg_points DESC "
                            "LIMIT 5;"
    )

    sql_rebounds_leaders = (
                            "SELECT P.name as Player, PSP.avg_rebounds as Rebounds "
                            "FROM Players P, Player_Season_Performance as PSP "
                            f"WHERE PSP.season = {selected_season} "
                            "AND PSP.player_id = P.player_id "
                            "ORDER BY PSP.avg_rebounds DESC "
                            "LIMIT 5;"
    )
    
    sql_assists_leaders = (
                            "SELECT P.name as Player, PSP.avg_assists as Assists "
                            "FROM Players P, Player_Season_Performance PSP "
                            f"WHERE PSP.season = {selected_season} "
                            "AND PSP.player_id = P.player_id "
                            "ORDER BY PSP.avg_assists DESC "
                            "LIMIT 5;"
    )

    sql_steals_leaders = (
                            "SELECT P.name as Player, PSP.avg_steals as Steals "
                            "FROM Players P, Player_Season_Performance PSP "
                            f"WHERE PSP.season = {selected_season} "
                            "AND PSP.player_id = P.player_id "
                            "ORDER BY PSP.avg_steals DESC "
                            "LIMIT 5;"
    )
                        
    sql_blocks_leaders = (
                            "SELECT P.name as Player, PSP.avg_blocks as Blocks "
                            "FROM Players P, Player_Season_Performance PSP "
                            f"WHERE PSP.season = {selected_season} "
                            "AND PSP.player_id = P.player_id "
                            "ORDER BY PSP.avg_blocks DESC "
                            "LIMIT 5;"
    )


    champion = query_db(sql_champion)['team'].tolist()
    st.write(f'The championship team of season {selected_season} is **{champion[0]}**')
    
    award_winners = query_db(sql_awards)
    st.write('The award-winners of the season:')
    st.dataframe(award_winners)

    points_leaders = query_db(sql_points_leaders)
    st.write('Scoring leaders of the season:')
    st.dataframe(points_leaders)

    rebounds_leaders = query_db(sql_rebounds_leaders)
    st.write('Rebound leaders of the season:')
    st.dataframe(rebounds_leaders)

    assists_leaders = query_db(sql_assists_leaders)
    st.write('Assist leaders of the season:')
    st.dataframe(assists_leaders)

    steals_leaders = query_db(sql_steals_leaders)
    st.write('Steal leaders of the season:')
    st.dataframe(steals_leaders)

    blocks_leaders = query_db(sql_blocks_leaders)
    st.write('Block leaders of the season:')
    st.dataframe(blocks_leaders)


"## Player information"
"### A player's average statistics over the past five seasons"
sql_players = "SELECT name from Players ORDER BY name;"
player_li = query_db(sql_players)['name'].tolist()
selected_player = st.selectbox("Choose an NBA player", player_li)
if selected_player:
    sql_stats = (
                    "SELECT P.name as Player, PSP.season as Season, PSP.avg_points as PPG, PSP.avg_rebounds as RPG, PSP.avg_assists as APG, PSP.avg_steals as SPG, PSP.avg_blocks as BPG " 
                    "FROM Players as P, Player_Season_Performance as PSP "
                    "WHERE PSP.season > 2015 "
                    "AND PSP.player_id = P.player_id "
                    f"AND P.name = '{selected_player}' "
                    "ORDER BY P.name ASC, PSP.season DESC;"
    )
    stats = query_db(sql_stats)
    st.dataframe(stats)


"### A player's career-high stats (in database only)"
input_player = st.text_input("Enter a player's name")
if input_player:
    sql_career_high = (
                        "SELECT P.name as Player, MAX(PGP.points) as career_high_points, MAX(PGP.rebounds) as career_high_Rebounds, MAX(PGP.assists) as career_high_Assists, MAX(PGP.steals) as career_high_Steals, MAX(PGP.blocks) as career_high_Blocks "
                        "FROM Players P, Player_Game_Performance PGP "
                        "WHERE P.player_id = PGP.player_id "
                        f"AND P.name LIKE '%{input_player}%' "
                        "GROUP BY P.name"
    )
    player_career_high = query_db(sql_career_high)
    st.dataframe(player_career_high)



'## Check two team battle history'
sql_teams_query = "SELECT DISTINCT(name) FROM Teams;"
team_li = query_db(sql_teams_query)['name'].tolist()
team1 = st.selectbox("Team one", team_li)
'### vs'
team2 = st.selectbox("Team two", team_li)

if team1 and team2:
    if team1 != team2:
        sql_games = (
                        "SELECT G.game_date as Date, H.name as Host, GU.name as Guest, G.score as Score, G.winner as Winner "
                        "FROM Games G, Teams H, Teams Gu "
                        "WHERE G.host_team_id = H.team_id "
                        "AND G.guest_team_id = Gu.team_id "
                        "AND ("
                            f"(H.name = '{team1}' AND Gu.name = '{team2}')"
                            "OR " 
                            f"(H.name = '{team2}' AND Gu.name = '{team1}')"
                        ");"
        )
        games = query_db(sql_games)
        st.dataframe(games)
    else:
        st.write("There should be two different teams!")











