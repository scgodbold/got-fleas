# Got Fleas

I got tired of looking at fleaflickers site to try and determine how many RBs I had, how many players do I have, ect. Often it would involve scrolling down the page and me losing count.

Got fleas is a feaflicker reporting tool that will fetch player data from a specified team on the site and return it to be processed and displayed in a report. To try and make it as flexible as possible I constructed report strings. This makes it possible to mix and match how you players are categorized, organized and displayed.

## Setup



## Reports

A report string follows a simple pattern.

```
Category.SortMethod.Aggregate
```

All report strings are case insensitive and everything besides the category are optional.

### Category [Required]

This is how the players are divided into buckets. Typically its something like position played or team they are a member of. The following are possible categories.

*Position* - Position played by the player

*Injury* - Groups players into injury status in the league

*Bye* - Group players based on which week they have a bye week

*Team* - Group players based on which team in the NFL they play for


### Sort Method

This is how the players are organized within the buckets. If omitted it defaults to organizing by position rank. Additionally the sort method data is displayed next to the players name within the table.

*Position Rank* - Players rank within their position type

*Bye* - Players ordered by their bye week

*Owned* - Players are ordered by the % of people on fleaflicker that own them

*Injury* - Playerse orderd by if they are injured

*Age* - Players are ordered by their age


### Aggregate

This displays in the column header and aggregates the information the players were sorted by. Defaults to number of players inside the given column

*Count* - Number of players in the column

*Max* - Largest value within the column (Does not work w/ injury sorted)

*Min* - Minimum value within the column (Does not work w/ injury sorted)

*Average* - Average value within the column (Does not work w/ injury sorted)
