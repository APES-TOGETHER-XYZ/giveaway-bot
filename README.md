# Discord Giveaway Bot
Simple Discord based giveaway bot.

## Setup
### Prerequisities
- Discord
- Heroku account

### Create a Discord application
- Go to https://discord.com/developers/applications
- Create a New Application
- Name it `Giveaway Bot` or a name of your choice
- Add an image, this will be the avatar of the bot
- Go to the `Bot` tab and click `Add Bot`
- Click `Reset Token`
- Copy the generated token and store it somewhere safe
- Disable `Public Bot`
- Enable all `Privileged Server Intents`
- Go to the `OAuth2` tab then `URL Generator` and select `bot` scope then `Manage Channels`
- Copy the `Generated URL` and paste it into your browser
- Select your server to add the bot to your server

### Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/APES-TOGETHER-XYZ/giveaway-bot)

- Enter a unique app name
- Enter your discord bot token from the previous setup
- Enter the emoji you want people to react with (copy and paste from the 'native' column [here](https://apps.timwhitlock.info/emoji/tables/unicode))
- Enter the image url that you want to be displayed as the icon for the giveaway message
- Click Deploy app
- Once done, click `Manage`
- Go to the `Resources` tab
- If the `worker` row is not enabled, click the edit icon and then enable it.
- Your bot should now be active in your server

## Running a giveaway

In a private channel, run `!giveaway` and follow the instructions.

When entering the channel name, be sure to include the `#`