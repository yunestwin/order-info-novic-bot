import os
import json
import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1konwN3p4TJ9uRnHqfsAbV4OJX4ZQgBDxgFASQkkFWPw/edit?usp=sharing").sheet1

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def info(ctx):
    await ctx.send("Please enter your order number:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    order_number = msg.content.strip()

    records = sheet.get_all_records()

    for row in records:
        if str(row["Order Number"]) == order_number:
            status = row["Delivery Status"]
            tracking = row["Tracking Link"]
            notes = row["Notes"]
            await ctx.send(
                f"**Order Number:** {order_number}\n"
                f"**Status:** {status}\n"
                f"**Tracking:** {tracking}\n"
                f"**Notes:** {notes}"
            )
            return

    await ctx.send("Order number not found.")

keep_alive()
bot.run("discord_token")