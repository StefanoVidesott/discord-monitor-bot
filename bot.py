import discord
from discord.ext import commands
import os

# Define intents to access member status updates
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration
USER_IDS_TO_MONITOR = [976193298387595274]
ADMIN_USER_ID = 618747601436540929
BOT_TOKEN = os.getenv('BOT_TOKEN')

previous_statuses = {}

STATUS_COLORS = {
    discord.Status.online: discord.Color.green(),
    discord.Status.offline: discord.Color.dark_gray(),
    discord.Status.idle: discord.Color.orange(),
    discord.Status.dnd: discord.Color.red(),
}

FRIENDLY_STATUS_NAMES = {
    discord.Status.online: "Online 🟢",
    discord.Status.offline: "Offline ⚫",
    discord.Status.idle: "Idle 🟡",
    discord.Status.dnd: "Do Not Disturb 🔴",
}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Monitoring user statuses...')
    for guild in bot.guilds:
        for member in guild.members:
            if member.id in USER_IDS_TO_MONITOR:
                previous_statuses[member.id] = member.status
                print(f'{member.name} is {member.status}')


@bot.event
async def on_presence_update(before, after):
    if after.id in USER_IDS_TO_MONITOR and before.status != after.status:
        try:
            admin_user = await bot.fetch_user(ADMIN_USER_ID)
            if admin_user:
                embed = discord.Embed(
                    title=f"Status Update for {after.name}",
                    description=f"{after.name} changed status:",
                    color=STATUS_COLORS.get(after.status, discord.Color.blue()),
                )
                embed.add_field(
                    name="Previous Status",
                    value=FRIENDLY_STATUS_NAMES.get(before.status, 'Unknown'),
                    inline=True
                )
                embed.add_field(
                    name="Current Status",
                    value=FRIENDLY_STATUS_NAMES.get(after.status, 'Unknown'),
                    inline=True
                )
                embed.set_footer(text="Status change detected")
                embed.timestamp = discord.utils.utcnow()
                await admin_user.send(embed=embed)

                previous_statuses[after.id] = after.status
        except Exception as e:
            print(f"Error sending status update: {e}")


if __name__ == '__main__':
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"Failed to start the bot: {e}")
