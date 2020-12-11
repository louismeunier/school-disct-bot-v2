** A Discord Bot **

Started off as Discord bot to get news and data from my school, but now is a large collection of utility and api-related functions.

To use this repository:
[] Clone it
[] Create a "secrets.json" file with the following keys:
    "DiscordToken":"YourDiscordToken",
    "BotPerms":{"Schedule":"IDOfWhoCanUpload"},
    "OtherTokens":{"CalendarID":"GoogleCalendarID"},
    "rssUrl":"URL of some rss feed (can be customized to have multiple quite easily)"
[] If you want to be able to use the Google Calendar API, go to https://developers.google.com/calendar/quickstart/python, create a new project, and downloads credentials.json into the utils/calendar_api folder.
[] Create a log.txt file in the main directory, if you want to enable error logs writing to a text file. If not, simple delete the ```on_command_error()``` function override in index.py