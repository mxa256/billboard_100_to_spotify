# Billboard 100 to Spotify
Python code to create Spotify playlists based on Billboard Top 100 songs on a date selected by the user.

This is relatively short code that accomplishes a lot. We use the Spotify API (must have client ID and client secret) and the Billboard API.

We first ask the user to provide a date. This is the date for which the Billboard Top 100 songs will be queried. We then scrape the Billboard website using Beautiful Soup to extract the top 100 songs and artists. We create a dictionary with these names/songs.

We then use Spotify API to create a new playlist that includes these top 100 songs. 

Note that some songs from the top 100 playlist cannot be added to Spotify because 1.) They are not available on Spotify, 2.) They are misspelled, 3.) Data is incorrect (i.e. an early release song may be listed on the Billboard list from the year 2000 but on Spotify it's listed as being released in 2001.
