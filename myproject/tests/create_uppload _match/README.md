# From Excel to SQL: Developing a Data-Driven Approach to Comprehensive Ranking and Analytics for Baby-Foot Games

Elo Rating System for any 2 VS 2 sport such as baby-foot.




## Project Description

This project is a new implementation of the Elo rating system in a 2 vs 2 game scenario, where each team is considered as a unique player with its own rating. The goal is to calculate the rating for each player and team based on their performance in past matches, and use this information to make predictions about future matches.

The project consists of several parts: 
- Data Processing: A script reads a CSV file containing the match data, processes it, and stores it in a database with an architecture designed for data visualization.

- Rating Calculation: The Elo rating system is used to calculate the rating for each player and team. The K-factor is determined based on the number of games played by the player or team, with a higher K-factor used for players or teams with fewer games played to allow for quicker adjustments to their ratings. The rating is then updated based on the outcome of the match and the ratings of the opposing teams.
- Web Component: A simple web app is used to collect data about the next match. This data is then processed by the script and added to the database, allowing for real-time updates to the ratings.
- Data Visualization: In addition to calculating ratings, this project also includes data visualization tools to allow for analysis of player and team performance over time. These tools include charts and graphs that display rating trends, win-loss ratios, and other useful information.

Overall, this project aims to provide a comprehensive solution for managing and analyzing player and team performance in a 2 vs 2 game scenario, using the Elo rating system and modern data visualization techniques.


## Authors

- [@lkolebka](https://www.github.com/lkolebka


## License

This application is available under the MIT License. See the [LICENSE](LICENSE) file for more information.

