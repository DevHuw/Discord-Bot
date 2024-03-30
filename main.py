# import all objectives
import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
import subprocess
import asyncio
import requests
import json



# load some basic vars
AUTH_FILE = "authenticated_users.txt"
load_dotenv()
DISCORD_TOKEN = os.getenv("TOKEN")
REPORT_FORM_LINK = "https://forms.gle/XkSsbV6Mn8jpcCRq5"
BAN_APPEAL_FROM_LINk = "https://forms.gle/vzDcdREX8c3k3Wuw8"
GAME_MOD_APP = "https://forms.office.com/r/r4Njy3qjhs"
GAME_MANAGER_APP = "https://forms.office.com/r/RNeTcThhrr"
DISCORD_MANAGER_APP = "https://forms.office.com/r/RNeTcThhrr"
CO_OWNER_APP = "https://forms.office.com/r/RNeTcThhrr"
COMMUNITY_MANAGER_APP = "https://forms.office.com/r/RNeTcThhrr"
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
activity = discord.Activity(type=discord.ActivityType.watching, name="/help")
bot = commands.Bot(command_prefix=".", intents=intents, activity=activity, status=discord.Status.online)
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




#status button embed gui
class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Startup", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=task_completed, ephemeral=True)
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
        await interaction.response.send_message(embed=task_completed, ephemeral=True)
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





# apply for staff button embed gui
class Jobs(discord.ui.View):
    def __init__(self):
        super().__init__()

        btn1 = discord.ui.Button(label="Game Moderator", style=discord.ButtonStyle.primary, url=GAME_MOD_APP)
        btn2 = discord.ui.Button(label="Game Manager", style=discord.ButtonStyle.primary, url=GAME_MANAGER_APP)
        btn3 = discord.ui.Button(label="Discord Manager", style=discord.ButtonStyle.primary, url=DISCORD_MANAGER_APP)
        btn4 = discord.ui.Button(label="Co Owner", style=discord.ButtonStyle.primary, url=CO_OWNER_APP)
        btn5 = discord.ui.Button(label="Community Manager", style=discord.ButtonStyle.primary, url=COMMUNITY_MANAGER_APP)
        self.add_item(btn1)
        self.add_item(btn2)
        self.add_item(btn3)
        self.add_item(btn4)
        self.add_item(btn5)






# ticket claim and close handling
class Ticket_Close(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

    async def on_timeout(self):
        pass


    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_id = interaction.channel_id
        channel = interaction.guild.get_channel(channel_id)

        if channel:
            embed = discord.Embed(
                title="Deleting Ticket",
                description="Thanks for using our ticket tool! \n You ticket will now be deleted",
                colour=discord.Color.red()
            )
            if interaction.message.author == bot.user:
                await interaction.message.delete()
            await interaction.response.send_message(embed=embed)
            await asyncio.sleep(delay=10)
            await channel.delete()



class Ticket_View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

    async def on_timeout(self):
        pass


    @discord.ui.button(label="🔒  Close", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = Ticket_Close()
        embed = discord.Embed(
            title="Close Ticket?",
            description="Are you sure you want to close the ticket?",
            colour=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, view=view)



    @discord.ui.button(label="🎟️  Claim", style=discord.ButtonStyle.primary)
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        support_role = discord.utils.get(interaction.guild.roles, name="support team")

        if support_role in interaction.user.roles:
            channel_id = interaction.channel_id
            channel = interaction.guild.get_channel(channel_id)
            new_category_id = 1223336507339837470  # Replace this with the ID of the new category
            new_category = interaction.guild.get_channel(new_category_id)
            if channel:
                old_name = channel.name
                old_name_convert = old_name.strip("unclaimed-")
                old_name_start = old_name.startswith("claimed-")
                try:
                    if interaction.user.display_name in old_name:
                        print("User not permitted: code 401")
                        embed = discord.Embed(
                            title="Could not claim ticket.",
                            description="You are not allowed to claim your own ticket!",
                            colour=discord.Color.red()
                        )
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        if old_name_start:
                            embed = discord.Embed(
                                title="Ticket Already Claimed!",
                                description="Sorry this ticket is already claimed!",
                                colour=discord.Color.red()
                            )
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                        else:
                            await channel.edit(name=f"claimed {old_name_convert}", category=new_category)
                            user = interaction.user.display_name
                            embed = discord.Embed(
                                title=f"{user} has claimed your ticket!",
                                description=f"{user} will now help you with what ever your problem is!",
                                colour=discord.Color.blue()
                            )
                    await interaction.response.send_message(embed=embed)
                except Exception as e:
                    print(f"Error occurred while editing channel name: {e}")
            else:
                print("No username found in channel name.")
        else:
            if support_role in interaction.user.roles:
                print("Channel not found: code 404")
                embed = discord.Embed(
                    title="Sorry! Something is wrong!",
                    description="Please contract huw7737 for help! \n Error Code: 404",
                    colour=discord.Color.from_rgb(r=255, g=0, b=0)
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                print("User not authorized: code 401")
                embed = discord.Embed(
                    title="Could not claim ticket.",
                    description="You are not allowed to claim your own ticket!",
                    colour=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)



# Support button embed gui
class Support(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

        btn1 = discord.ui.Button(label="🚫  Report Player Or Staff", url=REPORT_FORM_LINK, style=discord.ButtonStyle.primary)
        btn2 = discord.ui.Button(label="📩  Ban Appeal", style=discord.ButtonStyle.primary, url=BAN_APPEAL_FROM_LINk)

        self.add_item(btn1)
        self.add_item(btn2)

    async def on_timeout(self):
        pass

    @discord.ui.button(label="🎟️  Open General Ticket", style=discord.ButtonStyle.primary)
    async def open_ticket_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        support_role = discord.utils.get(interaction.guild.roles, name="support team")
        ticket_maker = interaction.user
        ticket_name = ticket_maker.name
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ticket_maker: discord.PermissionOverwrite(view_channel=True),
            support_role: discord.PermissionOverwrite(view_channel=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True)
        }

        # Check if a channel with the user's name already exists
        existing_channel_unclaimed = discord.utils.get(interaction.guild.text_channels, name=f"unclaimed-{ticket_name}")
        existing_channel_claimed = discord.utils.get(interaction.guild.text_channels, name=f"claimed-{ticket_name}")

        if existing_channel_unclaimed or existing_channel_claimed:
            # Disable the button and send a message indicating that a ticket already exists
            embed = discord.Embed(
                title="New Town City Support",
                description="Sorry, you already have a ticket open!",
                colour=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                unclaimed_tickets = interaction.guild.get_channel(1223336352129744896)
                ticket_channel = await unclaimed_tickets.create_text_channel(name=f"Unclaimed {ticket_name}", overwrites=overwrites)
                ticket_channel_id = ticket_channel.id
                ticket_link = f"[Go to ticket](https://discord.com/channels/{interaction.guild.id}/{ticket_channel_id})"
                ticket_embed = discord.Embed(
                    title="New Town City Support Ticket",
                    description="Please provide as much detail as possible!",
                    colour=discord.Color.blue()
                )
                support_ticket_embed = discord.Embed(
                    title="Ticket Created!",
                    description=f"Please provide as much detail as possible \n{ticket_link}",
                    colour=discord.Color.blue()
                )
                await interaction.response.send_message(embed=support_ticket_embed, ephemeral=True)
                view = Ticket_View()
                await ticket_channel.send(embed=ticket_embed, view=view)
                print(f"New ticket:{ticket_link}, {support_role}, {ticket_maker}, {ticket_name}, {ticket_channel_id}")
            except discord.errors.HTTPException as e:
                print(f"ERROR: FAILED TO CREATE NEW TICKET CHANNEL! FULL ERROR: {e}")



    @discord.ui.button(label="🖥️  Apply For Staff", style=discord.ButtonStyle.green)
    async def apply_for_staff_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = Jobs()
        await interaction.response.send_message(ephemeral=True, view=view)




# define reading and writing to authenticated_users.txt
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



#update member count
async def update_member_count():
    while True:
        guild = bot.get_guild(1221200110197674075)
        member_count = guild.member_count
        channel = bot.get_channel(1221213562270384240)
        await channel.edit(name=f"All Members: {member_count}")
        print(f"All Members: {member_count}")

        member_count2 = member_count - 2
        channel = bot.get_channel(1221213566150115422)
        await channel.edit(name=f"Members: {member_count2}")
        print(f"Members: {member_count2}")
        await asyncio.sleep(900)




# when bot starts it should print Logged in as username and should start running backend.py
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(bot.guilds)
    await support_reset_startup()
    #subprocess.Popen(["python", "backend.py"])
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    await update_member_count()



# when a user join do a few things
@bot.event
async def on_member_join(member):
    print(f"{member.name} Joined Server")
    un_verified = discord.utils.get(member.guild.roles, name="Unverified")
    await member.add_roles(un_verified, reason="New Server Member")
    verified = discord.utils.get(member.guild.roles, name="Member")
    banned_role = discord.utils.get(member.guild.roles, name="Banned_On_Roblox")
    bloxlink_api = f'https://api.blox.link/v4/public/guilds/1221200110197674075/discord-to-roblox/{member.id}'
    bloxlink_api_key = 'e44fb0bf-21ac-4ef8-8c4d-8cb1dcae378e'
    headers = {"Authorization": bloxlink_api_key}
    response = requests.get(bloxlink_api, headers=headers)
    data = response.json()
    print(data)

    if response.status_code == 404:
        print(f"ERROR: Could not verify {member.name} Bloxlink error")

    if response.status_code == 200:
        roblox_id = data['robloxID']
        print(roblox_id)
        roblox_api = f"https://users.roblox.com/v1/users/{roblox_id}"
        roblox_response = requests.get(roblox_api)
        print(roblox_response.json())
        roblox_data = roblox_response.json()
        user_description = roblox_data.get("description")
        user_created = roblox_data.get("created")
        user_isBanned = roblox_data.get("isBanned")
        user_hasVerifiedBadge = roblox_data.get("hasVerifiedBadge")
        user_name = roblox_data.get("name")
        user_displayName = roblox_data.get("displayName")
        user_link = f"https://www.roblox.com/users/{roblox_id}/profile"

        if roblox_response.status_code == 200:
            print(f"SUCCESS: Verified {member.name} as {user_displayName}")
            await member.remove_roles(un_verified)
            await member.add_roles(verified)
            await member.edit(nick=user_displayName)
            print(user_isBanned)

            if user_isBanned:
                await member.remove_roles(verified, reason="User is banned from roblox")
                await member.add_roles(banned_role, reason="User is banned from roblox")
                print(f"WARN: {member.name} or {user_name} or {user_displayName} at {user_link} is banned from roblox!")
                huw = bot.get_user(618331718692241408)
                offender = bot.get_user(member.id)
                await offender.send(
                    f"Hey! \n \n Welcome to new town city discord server! \n \n But you're banned from roblox :( so that means that you have been suspended from our discord server. \n \n If you want to be unsuspended you should: \n - keep you're DM's open \n - wait for staff member to DM you (DO NOT ping members of staff!) \n - reply to all of the staff members questions \n - if you do all this there still is a chance you will not be unsuspended because being banned from ROBLOX is against our rules!")
                await huw.send(
                    f"WARN: Discord member: {member.name} with roblox names: {user_name} and {user_displayName} at roblox profile link: {user_link} is banned from roblox!")
        else:
            print(f"ERROR: Could not verify {member.name} Roblox error")
    else:
        print(f"ERROR: Could not verify {member.name} Full Error")




# sets the support message
async def support_reset_startup():
    authenticated_users = await read_authenticated_users()
    guild = bot.guilds[0]
    support_channel = guild.get_channel(1223250744216649818)

    if authenticated_users and support_channel:
        view = Support()

        await support_channel.purge(limit=None)

        embed = discord.Embed(
            title="New Town City Support",
            description="Welcome to New Town City support! \n \n In order to speed up our support process, please choose from one of the support categories listed below! Our staff team is ready to assist you with any issues you may be experiencing. \n \n Please DO NOT DM staff members unless the tool is not working. Use support tickets for a faster response. Please only open one ticket at a time!",
            colour=discord.Color.blue()
        )

        await support_channel.send(embed=embed, view=view)




# resets the support embed gui
@bot.tree.command(name="lookup", description="Looks up discord user and outputs their roblox profile")
async def lookup(interaction: discord.Interaction, user: discord.Member):
    authenticated_users = await read_authenticated_users()
    bloxlink_api = f'https://api.blox.link/v4/public/guilds/1221200110197674075/discord-to-roblox/{user.id}'
    bloxlink_api_key = 'e44fb0bf-21ac-4ef8-8c4d-8cb1dcae378e'

    if interaction.user.id in authenticated_users:
        try:
            headers = {"Authorization": bloxlink_api_key}
            response = requests.get(bloxlink_api, headers=headers)
            response.raise_for_status()  # Raise HTTPError for 4xx and 5xx status codes
            data = response.json()
            print(data)


            if roblox_response.status_code == 200:
                roblox_id = data['robloxID']
                print(roblox_id)
                roblox_api = f"https://users.roblox.com/v1/users/{roblox_id}"
                roblox_response = requests.get(roblox_api)
                print(roblox_response.json())
                roblox_data = roblox_response.json()
                user_description = roblox_data.get("description")
                user_created = roblox_data.get("created")
                user_isBanned = roblox_data.get("isBanned")
                user_hasVerifiedBadge = roblox_data.get("hasVerifiedBadge")
                user_name = roblox_data.get("name")
                user_displayName = roblox_data.get("displayName")



            embed = discord.Embed(
                title=f"Discord ID: {user.id} \nRoblox ID: {roblox_id} \nhttps://www.roblox.com/users/{roblox_id}/profile",
                colour=discord.Color.blue(),
                description=f"Description: {user_description} \n \n Account Created: {user_created} \n \n Banned? {user_isBanned} \n \n Verified Badge? {user_hasVerifiedBadge} \n \n Username: {user_name} \n \n Display Name: {user_displayName}"
            )
            print("DEBUG: Loading message ready to send to user")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print("DEBUG: Sent")
        except requests.exceptions.HTTPError as e:
            print(f"ERROR: {e}")
            if e.response.status_code == 404:
                # User not found, handle accordingly
                embed = discord.Embed(
                    title="User not found",
                    colour=discord.Color.red()
                )
                try:
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                except discord.errors.NotFound:
                    print("DEBUG: Interaction not found")
            else:
                # Handle other HTTP errors if needed
                await interaction.response.send_message("An error occurred while processing your request", ephemeral=True)




# resets the support embed gui
@bot.tree.command(name="support_reset", description="Creates/Resets the support GUI")
async def support_reset(interaction: discord.Interaction):
    authenticated_users = await read_authenticated_users()
    support_channel = bot.get_channel(1223250744216649818)

    if interaction.user.id in authenticated_users:

        view = Support()

        await support_channel.purge(limit=None)

        embed = discord.Embed(
            title="New Town City Support",
            description="Welcome to New Town City support! \n \n In order to speed up our support process, please choose from one of the support categories listed below! Our staff team is ready to assist you with any issues you may be experiencing. \n \n Please DO NOT DM staff members unless the tool is not working. Use support tickets for a faster response. Please only open one ticket at a time!",
            colour=discord.Color.blue()
        )

        await interaction.response.send_message(",./!*&")
        await support_channel.send(embed=embed, view=view)
        if support_channel:
            async for message in support_channel.history(limit=None):
                if ",./!*&" in message.content.lower():
                    await message.delete()
                    print("LOG: Response Message Deleted For /support_reset")



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
@bot.tree.command(name="help", description="View all the commands for this bot")
async def help(interaction: discord.Interaction):
    commands_embed = discord.Embed(
        title="NTC Commands",
        description="/help (shows the list of commands) \n /auth (authenticates users to use NTC commands) \n /remove (removes users from the auth list) \n /announcement (posts an announcement in the channel) \n /support_rest (resets the ticket support sys) \n /reload_cfg (reloads the bots config) \n /status (changes the servers status) \n /close (closes the ticket) \n /claim (claims the ticket)",
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
