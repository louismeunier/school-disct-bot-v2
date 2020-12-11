**____Bot**

Started off as Discord bot to get news and data from my school, but now is a large collection of utility and api-related functions.


To use this repository:



* Clone the repository with `git clone https://github.com/louismeunier/school-disct-bot-v2` or click `Code` in the top right.



* Create a `secrets.json` file in the base repository with the following structure:

```
    {
        "DiscordToken":"YourDiscordToken",


        "BotPerms":{"Schedule":"IDOfWhoCanUpload"},


        "OtherTokens":{"CalendarID":"GoogleCalendarID"},


        "rssUrl":"URL of some rss feed (can be customized to have multiple quite easily)"
    }

```
* If you want to be able to use the Google Calendar API, go to https://developers.google.com/calendar/quickstart/python, create a new project, and downloads `credentials.json` into the `utils/calendar_api folder`.



* Create a log.txt file in the main directory, if you want to enable error logs writing to a text file. If not, simple delete the ```on_command_error()``` function override in `index.py`



* Run  `python3 -m pip install -r requirements.txt`


I'm not 100% sure if this bot could work in python2, but it was developed in python 3.8.3, so all the behavior is based around that.





**Future Ideas**

*Open an issue if you have something you'd like me to add :)*

- [] Spotify API full implementation

- [] "Fun" cog with less useful but still cool function

- [] Re-write SoundCog to automatically create functions based on the contents of the `sounds` folder; may be very hard/impossible

- [] Expand RSS feed to allow for multiple feeds

