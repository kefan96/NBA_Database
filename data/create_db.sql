-- Principles of Database Systems
-- Course Project
-- Authors: Kefan Yang, Pinshuo Ye

DROP TABLE IF EXISTS Arenas CASCADE;
DROP TABLE IF EXISTS Teams CASCADE;
DROP TABLE IF EXISTS Players CASCADE;
DROP TABLE IF EXISTS Owners CASCADE;
DROP TABLE IF EXISTS Coaches CASCADE;
DROP TABLE IF EXISTS Seasons CASCADE;
DROP TABLE IF EXISTS Games CASCADE;
DROP TABLE IF EXISTS Awards CASCADE;
DROP TABLE IF EXISTS Player_Wins_Award CASCADE;
DROP TABLE IF EXISTS Player_Game_Performance CASCADE;
DROP TABLE IF EXISTS Player_Season_Performance CASCADE;


CREATE TABLE Arenas (
    name        varchar(100),
    city        varchar(50),
    build_in    int,
    capacity    int,
    PRIMARY KEY (name, city)
);

CREATE TABLE Teams (
    team_id     varchar(50)     PRIMARY KEY,
    name        varchar(50)     NOT NULL,
    conference  varchar(50)     NOT NULL,
    division    varchar(50)     NOT NULL,
    arena_name  varchar(100),
    arena_city  varchar(100),
    FOREIGN KEY (arena_name, arena_city) REFERENCES Arenas(name, city) 
);

CREATE TABLE Players (
    player_id       varchar(50)   PRIMARY KEY,
    name            varchar(50)   NOT NULL,
    dob             date       ,
    jersey_number   int,
    position        varchar(50),
    year_in_league  int,
    team_id         varchar(50),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE Owners (
    owner_id    varchar(50)     PRIMARY KEY,        
    name        varchar(50)     NOT NULL,
    team_id     varchar(50),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE Coaches (
    coach_id    varchar(50)     PRIMARY KEY,
    name        varchar(50)     NOT NULL,
    coach_since int,
    team_id     varchar(50),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE Seasons (
    year                int         PRIMARY KEY,
    start_date          date,
    end_date            date,
    champion_team_id    varchar(50),
    FOREIGN KEY (champion_team_id) REFERENCES Teams(team_id)
);

CREATE TABLE Games (
    game_id         varchar(50)     PRIMARY KEY,
    game_date       date,
    host_team_id    varchar(50)     NOT NULL,
    guest_team_id   varchar(50)     NOT NULL,
    season          int             NOT NULL,
    score           varchar(50),
    winner          varchar(50),
    FOREIGN KEY (host_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (guest_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (season) REFERENCES Seasons(year)
);

CREATE TABLE Awards (
    name            varchar(100)     PRIMARY KEY
);

CREATE TABLE Player_Wins_Award (
    player_id       varchar(50),
    award           varchar(50),
    season          int,
    PRIMARY KEY (player_id, award, season),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (award) REFERENCES Awards(name),
    FOREIGN KEY (season) REFERENCES Seasons(year)
);

CREATE TABLE Player_Game_Performance (
    player_id   varchar(50),
    game_id     varchar(50),
    points      int,
    rebounds    int,
    assists    int,
    blocks      int,
    steals      int,
    PRIMARY KEY (player_id, game_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

CREATE TABLE Player_Season_Performance (
    player_id       varchar(50),
    season          int,
    avg_points      decimal,
    avg_rebounds    decimal,
    avg_assists    decimal,
    avg_blocks      decimal,
    avg_steals      decimal,
    PRIMARY KEY (player_id, season),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (season) REFERENCES Seasons(year) 
);

-- cat arenas.csv | psql -U ky1323 -d ky1323-db -h localhost -p 5432 -c "COPY arenas from STDIN CSV HEADER"
-- cat teams.csv | psql -U ky1323 -d ky1323-db -h localhost -p 5432 -c "COPY teams from STDIN CSV HEADER"
-- cat awards.csv | psql -U ky1323 -d ky1323-db -h localhost -p 5432 -c "COPY awards from STDIN CSV HEADER"
-- cat coaches.csv | psql -U ky1323 -d ky1323-db -h localhost -p 5432 -c "COPY coaches from STDIN CSV HEADER"
-- cat owners.csv | psql -U ky1323 -d ky1323-db -h localhost -p 5432 -c "COPY owners from STDIN CSV HEADER"
-- cat seasons.csv | psql -U ky1323 -d ky1323-db -h localhost -p 5432 -c "COPY seasons from STDIN CSV HEADER"
-- cat players.csv | psql -U ky1323 -d ky1323-db -h localhost -p 5432 -c "COPY players from STDIN CSV HEADER"
-- cat games.csv | psql -U ky1323 -d ky1323-db -h localhost -p 5432 -c "COPY games from STDIN CSV HEADER"