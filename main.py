# import all objectives
import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import subprocess
import asyncio



# define some basic commands
AUTH_FILE = "authenticated_users.txt"
load_dotenv()
DISCORD_TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
activity = discord.Activity(type=discord.ActivityType.watching, name="/help")
bot = commands.Bot(command_prefix=".",intents=intents, activity=activity, status=discord.Status.online)
timeout_embed = discord.Embed(
    title="Timeout",
    description="Sorry, you took too long to respond.",
    colour=discord.Color.red()
)
sent_dm = discord.Embed(
    title="Sent in DM's",
    description="Please check your DM's to continue!",
    colour=discord.Color.blurple()
)
perm_error = discord.Embed(
    title="Error",
    description="error: you don't have the permissions to use this command!",
    colour=discord.Color.red()
)
want_to_continue = discord.Embed(
    title="Continue?",
    description="Do you want to continue with this operation? \n y/n",
    colour=discord.Color.blue()
)
task_completed = discord.Embed(
    title="Task Completed",
    colour=discord.Color.green()
)


#define some classes
class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Startup", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=task_completed)
        channel = bot.get_channel(1222911491821277276)
        status = bot.get_channel(1223028334170996826)
        embed = discord.Embed(
            title="Server Status: Online",
            description="Server Startup! \n Join in erlc with code: NTC",
            colour=discord.Color.green()
        )
        async for message in channel.history(limit=None):
            await message.delete()
        await status.edit(name="Server Status: Online")
        await channel.send(embed=embed)
        await channel.send("@everyone Server Has Started!", delete_after=5)
        await channel.last_message.delete()

    @discord.ui.button(label="Shutdown", style=discord.ButtonStyle.danger)
    async def shutdown(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=task_completed)
        channel = bot.get_channel(1222911491821277276)
        status = bot.get_channel(1223028334170996826)
        embed = discord.Embed(
            title="Server Status: Offline",
            description="Server Is Offline.",
            colour=discord.Color.red()
        )
        async for message in channel.history(limit=None):
            await message.delete()
        await status.edit(name="Server Status: Offline")
        await channel.send(embed=embed)


# define reading and writing to/from authenticated_users.txt
async def read_authenticated_users():
    try:
        with open(AUTH_FILE, "r") as file:
            lines = file.readlines()
            authenticated_users = [int(line.strip()) for line in lines]
            return authenticated_users
    except FileNotFoundError:
        return []

async def write_authenticated_users(authenticated_users):
    with open(AUTH_FILE, "w") as file:
        for user_id in authenticated_users:
            file.write(str(user_id) + "\n")





# when bot starts it should print Logged in as username and should start running backend.py
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    #subprocess.Popen(["python", "backend.py"])
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)





# announcement slash command
@bot.tree.command(name="announcement", description="Post an announcement")
async def announcement(interaction: discord.Interaction):
    authenticated_users = await read_authenticated_users()
    announcements_channel = bot.get_channel(1221208182186184904)

    if interaction.user.id in authenticated_users:
        await interaction.response.send_message(embed=sent_dm, ephemeral=True)

        title_embed = discord.Embed(
            title="Selected Announcement",
            description="Announcement has been selected. \n Please provide a title.",
            color=discord.Color.blue()
        )
        await interaction.user.send(embed=title_embed)

        try:
            title_response = await bot.wait_for('message', check=lambda message: message.author == interaction.user and isinstance(message.channel, discord.DMChannel), timeout=30.0)

            if title_response.content:
                # Prompt for description
                description_embed = discord.Embed(
                    title="Announcement Description",
                    description="Please provide a description for the announcement.",
                    color=discord.Color.blue()
                )
                await interaction.user.send(embed=description_embed)

                try:
                    description_response = await bot.wait_for('message', check=lambda message: message.author == interaction.user and isinstance(message.channel, discord.DMChannel), timeout=30.0)

                    # Check if a description is provided
                    if description_response.content:
                        # Post the announcement in the server's announcements channel
                        if announcements_channel:
                            announcement_embed = discord.Embed(
                                title=title_response.content,
                                description=description_response.content,
                                color=discord.Color.blue()
                            )
                            announcement_embed.set_author(name=f"by " + interaction.user.name, url=interaction.client.user.avatar.url)
                            await announcements_channel.send("@test")
                            await announcements_channel.send(embed=announcement_embed)
                            embeduserannounce = discord.Embed(
                                title="Announcement Posted!",
                                description="Your Announcement has been posted [check it out](<https://discord.com/channels/1221200110197674075/1221208182186184904>)",
                                colour=discord.Color.green()
                            )
                            await interaction.user.send(embed=embeduserannounce)
                        else:
                            embed = discord.Embed(
                                title="Could not find announcement channel",
                                description="Please contact huw7737 for help",
                                colour=discord.Color.red()
                            )
                            await interaction.user.send(embed=embed)
                    else:
                        await interaction.user.send(embed=timeout_embed)
                except asyncio.TimeoutError:
                    await interaction.user.send(embed=timeout_embed)
            else:
                await interaction.user.send(embed=timeout_embed)
        except asyncio.TimeoutError:
            await interaction.user.send(embed=timeout_embed)
    else:
        await interaction.response.send_message(embed=perm_error)




# status slash command
@bot.tree.command(name="status", description="Change the servers status")
async def status(interaction: discord.Interaction):
    authenticated_users = await read_authenticated_users()

    if interaction.user.id in authenticated_users:
        await interaction.response.send_message(embed=sent_dm, ephemeral=True)

        embed = discord.Embed(
            title="Server Status",
            description="Do you want to start or stop the server?",
            color=discord.Color.blue()
        )
        buttons = Buttons()
        await interaction.user.send(embed=embed, view=buttons)




# auth slash command
@bot.tree.command(name="auth", description="add users to auth list")
async def auth(interaction: discord.Interaction):
    supervisor_role = discord.utils.get(interaction.guild.roles, name="supervisor")
    authenticated_users = await read_authenticated_users()

    if supervisor_role in interaction.user.roles and int(interaction.user.id) in authenticated_users:
        embed = discord.Embed(
            title="New Town City Support",
            description="You are already authenticated!",
            color=discord.Color.yellow()  # You can customize the color if needed
        )
        await interaction.user.send(embed=embed)
        await interaction.response.send_message(embed=sent_dm, ephemeral=True)
    elif supervisor_role in interaction.user.roles:
        # User has the "supervisor" role, proceed with the command
        embed = discord.Embed(
            title="New Town City Support",
            description="You have authenticated with NTC support system!",
            color=discord.Color.green()  # You can customize the color if needed
        )
        await interaction.user.send(embed=embed)
        await interaction.response.send_message(embed=sent_dm, ephemeral=True)

        authenticated_users.append(interaction.user.id)
        print(f"Debug: userid is ", interaction.user.id)
        await write_authenticated_users(authenticated_users)
    else:
        # User does not have the required role, send a message indicating the restriction
        await interaction.response.send_message(embed=perm_error, ephemeral=True)
        await interaction.user.send(embed=perm_error)





# remove slash command
@bot.tree.command(name="remove", description="Remove user IDs from auth")
async def remove(interaction: discord.Interaction, userid: str):

    owner_role = discord.utils.get(interaction.guild.roles, name="Owner")
    print("userid is ", userid)

    try:
        authenticated_users = await read_authenticated_users()
        if owner_role in interaction.user.roles and int(userid) in authenticated_users:
            await interaction.response.send_message(embed=sent_dm, ephemeral=True)
            authenticated_users.remove(int(userid))
            await write_authenticated_users(authenticated_users)

            confirmation_embed = discord.Embed(
                title="Success",
                description=f"User with ID {userid} was removed from authenticated users.",
                color=discord.Color.green()
            )
            await interaction.user.send(embed=confirmation_embed)

        elif owner_role in interaction.user.roles:
            not_found_embed = discord.Embed(
                title="Error",
                description=f"User with ID {userid} is not in the list of authenticated users.",
                colour=discord.Color.red()
            )
            await interaction.response.send_message(embed=sent_dm, ephemeral=True)
            await interaction.user.send(embed=not_found_embed)
        else:
            await interaction.response.send_message(embed=perm_error, ephemeral=True)
            await interaction.user.send(embed=perm_error)

    except Exception as e:
        print(e)




# help slash command
@bot.tree.command(name="help", description="View all the commmands for this bot")
async def help(interaction: discord.Interaction):
    commands_embed = discord.Embed(
        title="NTC Commands",
        description="/commands (shows the list of commands) \n /auth (authenticates users to use NTC commands) \n /remove (removes users from the auth list) \n /post (gives options to post updates and SSU's) \n /support (open a support tick for NTC)",
        color=discord.Color.blue()
    )
    user=interaction.user
    await user.send(embed=commands_embed)
    await interaction.response.send_message(embed=sent_dm, ephemeral=True)


# reload_cfg slash command
@bot.tree.command(name="reload_cfg", description="Reloads the bots config")
async def reload_cfg(interaction: discord.Interaction):
    authenticated_users = await read_authenticated_users()


    if interaction.user.id in authenticated_users:
        vc_channel = bot.get_channel(1223028334170996826)
        channel = bot.get_channel(1222911491821277276)
        async for message in channel.history(limit=None):
            await message.delete()
        embed = discord.Embed(
            title="Server Status: Unknown",
            description="The server's status is: unknown",
            colour=discord.Color.blurple()
        )
        await vc_channel.edit(name="Server Status: unknown")
        await channel.send(embed=embed)  # Await the send() coroutine
        embed = discord.Embed(
            title="Task finished successfully",
            colour=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)  # Await the send_message() coroutine
    else:
        await interaction.response.send_message(embed=perm_error, ephemeral=True)  # Await the send_message() coroutine



# start bot loop
bot.run(DISCORD_TOKEN)