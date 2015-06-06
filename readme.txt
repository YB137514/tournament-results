****Swiss style tournament simulation module **** 

***Features.****
Provided module implements Swiss style tournament simulation.
In the Swiss style tourament no player is eliminated after a loss.
Database schema prevents rematches between players in the same tournament.
Player standings after each round is calculated by the PostgreSQL database server and not by python interpreter running on client machine. 

***Requirements:***
Python 2.7 or later version installed.
psycopg2 DB API 
PostgreSQL 9.3.6 or later installed
Bleach--HTML sanitizing library

***Quick start:***
First: Run the following on the command line:
psql  -- Opens client console of the PostgreSQL database
\i tournament.sql -- Creates database and all necessary relationships
\q --Exits PostgreSQL console

Second: Navigate to downloaded tournament folder: 
To run Swiss style tournament simulation execute: python sim.py on the command line
To run Unit Tests execute: python tourament_test.py on the command line

Comments regarding sim.py execution:
Simulation is designed to throw an error (psycopg2.IntegrityError) when there is repeat match between players. In this case run the simulation again until random drawing of winners and losers is such that there are no repeat matches between players.


***What's included:***
tournament.sql--database schema
tournament.py --implementation of a Swiss-system tournament
tournament_test.py--Unit Tests for functions in tournament.py
sim.py--Provided example of possible simulation code
readme.txt