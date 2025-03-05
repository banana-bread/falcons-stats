DROP TABLE IF EXISTS goal_scorers;
DROP TABLE IF EXISTS divisions;

CREATE TABLE divisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    division_id INTEGER NOT NULL,
    division_name TEXT NOT NULL
);

CREATE TABLE goal_scorers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    division_id INTEGER NOT NULL,
    player_name TEXT NOT NULL,
    team_name TEXT NOT NULL,
    goals INTEGER NOT NULL,
    FOREIGN KEY (division_id) REFERENCES divisions (division_id)
);