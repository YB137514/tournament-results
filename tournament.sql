-- Table definitions for the tournament project.


drop database tournament;
create database tournament;
\c tournament;


create table Players (
	   ID serial primary key,
	   name text
);


--View to return number of players currently registered
create view num_registered as
       select count(*) from Players;


--Table matches has 2 primary keys to prevent rematch between 
--the same players.
create table Matches (
	   match_ID serial,
	   player_1_ID integer, 
	   player_2_ID integer,
	   winner integer references Players,
	   primary key(player_1_ID, player_2_ID)	
);


--Query to count number of wins for each player
create view number_of_wins as 
select ID, name, count(winner) as num_of_wins
from Players left join Matches
on winner = ID
group by ID
order by num_of_wins desc;


--Query to count losses for each player 
create view number_of_losses as 
select ID, name, count(player_2_ID) as num_of_losses
from Players left join Matches
on player_2_ID = ID
group by ID
order by num_of_losses desc;


--Number of matches played for each player is the total 
--of their number of wins and number of losses. 
--Joining 2 previous view to calculate this result
create view number_of_matches as 
select number_of_wins.ID, sum(num_of_wins + num_of_losses) as matches_played
from number_of_wins inner join number_of_losses
on number_of_wins.ID = number_of_losses.ID
group by number_of_wins.ID;


--View to populate the standings table. 
create view StandingsView as
select number_of_wins.ID, name, num_of_wins, matches_played
from number_of_wins inner join number_of_matches
on number_of_wins.ID = number_of_matches.ID
order by num_of_wins desc;


create table Standings(
	player_ID integer primary key,
	name text,
	num_of_wins integer,
	num_of_matches_played integer	
);
