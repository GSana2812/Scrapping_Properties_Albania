## Scrapping Property Prices in Albania

In this project, I wanted to perform a regression task, trying to predict the property prices in Albania.
The data is obtained from 21century, the most reliable and successful real estate agency operating currently
in Albania. The scraping process gave me uniform results, precisely with these columns:
-Gross Area
-Interior Area
-Bedrooms
-Baths
-Floor-
-Type (Apartment, Land, etc)
-Status (New, Under Construction, etc)
-Price 
-City

At first, I got more than 6k results (initial_data_real_estate.csv), but then since I wanted to perform some predictive
analytics, and since a lot of price values were empty, unfortunately I had to dropped all the examples with the target variable
values (Price) as empty. This left me with only 2650, which can be satisfiable for a simple regression task, but nonetheless,
there were more empty price values than there were actual number. This came, because the real estate agents, didn't publish
the price, or the price section was denominated as "Price upon request". Besides that, its a very good dataset to observe some interesting
insights about the real estate situation in Albania. This and prediction can occur in a near future, but so far, I concluded something
extremely interesting.

1. Eventhough everyone would think, this would be a suitable regression task, actually the price variable, comes in fixed values (5),
so one may conceptually think this problem, as a multi classification task, instead of a regression one.
2. The same thing, would happen with the areas, they are so static and fixed, leaving me with the impression, that all houses
built recently in Albania, seem to be so well-structured, price and size based. 

Of course this project, can be extended further, but I was more interesting for a regression task. In the future
I may go back and deal with this classification problem. For now, the project consists in a dataset creation 
providing us with interesting content and what scrapping is really able to do.