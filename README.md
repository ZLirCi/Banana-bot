# Banana-bot
A Telegram bot for tracking and managing numerical data, using Google Sheets as a database to store entries and calculate balances.

Project Description

This project is a Telegram bot designed to track and manage various numerical values. Users can add any kind of data, and the bot automatically stores it while maintaining a running balance linked to the date and the user’s name.

The idea behind this project was to create a simple and flexible tracking tool — for example, for expenses, points, or any other numerical metrics.

The bot operates through a command-based system, where users enter commands directly into the chat. The main commands include:

/set — adds a new entry
/balance — shows the current balance
/remove — deletes a specific entry
/removeall — deletes all user entries
/history — displays the full history of records

How it works

From a technical perspective, the process works as follows:

When a user sends a command, it is delivered to Telegram’s servers. The bot, using a secure token, retrieves the message and determines which action needs to be performed.

Next, the bot sends a request to a Google Sheet, which acts as the database. All user records are stored there.

The Google Sheet processes the request — for example, checking for existing data or updating information — and sends a response back to the bot.

Finally, the bot formats this response into a user-friendly message and sends it back to the user in Telegram.

In this way, the bot connects Telegram with Google Sheets, providing a simple and automated solution for data tracking.
