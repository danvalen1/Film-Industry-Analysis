# Analysis of Film Industry ROIs
**Authors**: Malcolm Katzenbach, Lauren Phipps, Dan Valenzuela

## Data Understanding
For the purposes of this analysis we focused primarily on data from the Internet Movie Database (IMDB) and The-Numbers.com (TN), two sources that focus on the film industry. Specifically we used datasets that included--on one hand--title, date released, and genre data and--on the other hand--title, date released, production budgets, and box office figures. Below is a summary of the data pertinent to our analysis broken down by file. 

| imdb.title.basics.csv | tn.movie_budgets.csv |
| --- | --- |
| primary_title | movie |
| start_year | release_date |
| genres |  |
|  | production_budget |
|  | domestic_gross |
|  | worldwide_gross |


## Evaluation 

The overall business problem that was given asked how a new movie studio may be as successful as possible. By looking more deeply into the data on movies from the past 10 years, the analysis has shown what types of genres have done well with certain sized budgets. This successfully has answered the main question in a basic. This analysis is helpful as done, however there are certain areas that could bring more accuracy to the analysis. 

    -The Advertisement Cost: In the analysis, it was assumed that advertisement budget was equal to the production budget. However, it unlikely that all movies had an equal advertisement and production budget. By using the    exact advertisement budget, it will increase the accuracy of the ROI.
    -Inflation: This analysis did not account for inflation. While only over a 10 year period, the inflation would have an effect on the money values of the movies, which would increase the accuracy of the comparison between  movies.
    -Time Period of Analysis: As mentioned before, the dataframes were only for movies from the last 10 years.     While useful for immediate future movies, having a longer period of data could increase how robust our analysis is.
    -Box Office Only: This data only takes into account of the box office. If Microsoft desired to go into         streaming services and produce movies for the streaming service only, it would be more accurate to include data on streamed movies.
    
    
## Conclusion

This analysis brings forward two recommendations:

**Produce high budget adventure films-** if the studio has a high production & advertisement budget, adventure films had the highest median ROI for high budgets

**Produce low budget thrillers-** if the studio has a low budget, thrillers have the highest possible ROI of any genre


## Next Steps

**Evaluating personnel that maximize ROI-** By analyzing the personnel of successful movies in genres such as thrillers and adventures, the studio could attempt to hire those that would most likely help produce a movie with a high ROI.

**Find accurate advertisement budgets for movies and account for inflation-** By going back into the analysis, the accuracy of the ROIs could be increased.

**Constructing Portfolios of Films-** With a budget, a portfolio of films could be maximized for ROI by genre and budget.
