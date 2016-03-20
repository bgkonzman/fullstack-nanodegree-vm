-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name TEXT);

CREATE TABLE matches (winner INTEGER REFERENCES players (id),
                      loser INTEGER REFERENCES players (id));

CREATE VIEW standings AS
    SELECT id,
        name,
        SUM(CASE WHEN id = winner THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN id = winner OR id = loser THEN 1 ELSE 0 END) AS matches
    FROM players LEFT JOIN matches
    ON id = winner OR id = loser
    GROUP BY id
    ORDER BY wins DESC, matches DESC;
