# discordcss/cli.py

import re
import discord
from discord.ext import commands
import argparse

def extract(css_path):
    with open(css_path, 'r') as file:
        css_content = file.read()

    # .client extraction logic
    client_pattern = re.compile(r'\.client\s*{\s*([^}]+)\s*}', re.DOTALL)
    client_match = client_pattern.search(css_content)

    if client_match:
        client_block_content = client_match.group(1)

        token_match = re.search(r'token:\s*"([^"]+)"', client_block_content)
        prefix_match = re.search(r'prefix:\s*"([^"]+)"', client_block_content)

        if token_match and prefix_match:
            global token
            global bot
            token = token_match.group(1)
            prefix = prefix_match.group(1)

            bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
        else:
            print("Token or prefix not found in .client block.")
    else:
        print(".client block not found in the CSS file.")

    # .command extraction logic
    command_pattern = re.compile(r'\.command\s*{\s*([^}]+)\s*}', re.DOTALL)
    command_matches = command_pattern.finditer(css_content)

    for command_match in command_matches:
        command_block_content = command_match.group(1)

        command_match = re.search(r'command:\s*"([^"]+)"', command_block_content)
        response_match = re.search(r'response:\s*"([^"]+)"', command_block_content)
        description_match = re.search(r'description:\s*"([^"]+)"', command_block_content)

        if command_match and response_match and description_match:
            command = command_match.group(1)
            response = response_match.group(1)
            description = description_match.group(1)

            @bot.command(name=command, help=description)
            async def custom_command(ctx, response=response): 
                await ctx.send(response)
        else:
            print("Command, response, or description not found in .command block.")

    # .onjoin extraction logic
    onjoin_pattern = re.compile(r'\.onjoin\s*{\s*([^}]+)\s*}', re.DOTALL)
    onjoin_matches = onjoin_pattern.finditer(css_content)

    for onjoin_match in onjoin_matches:
        onjoin_block_content = onjoin_match.group(1)

        response = re.search(r'response:\s*"([^"]+)"', onjoin_block_content)
        channelid = re.search(r'channel_id:\s*"([^"]+)"', onjoin_block_content)

        if response:
            response = response.group(1)

            @bot.event
            async def on_member_join(member):
                channel = bot.get_channel(channelid)
                formatted_response = response.format(member_count=len(channel.guild.members), member=member.mention)
                await channel.send(formatted_response)
        else:
            print("Response not found in .onjoin block.")

    # .onleave extraction logic
    onleave_pattern = re.compile(r'\.onleave\s*{\s*([^}]+)\s*}', re.DOTALL)
    onleave_matches = onleave_pattern.finditer(css_content)

    for onleave_match in onleave_matches:
        onleave_block_content = onleave_match.group(1)

        response = re.search(r'response:\s*"([^"]+)"', onleave_block_content)
        channelid = re.search(r'channel_id:\s*"([^"]+)"', onleave_block_content)

        if response:
            response = response.group(1)

            @bot.event
            async def on_member_leave(member):
                channel = bot.get_channel(channelid)
                formatted_response = response.format(member_count=len(channel.guild.members), member=member.mention)
                await channel.send(formatted_response)
        else:
            print("Response not found in .onleave block.")

def main():
    parser = argparse.ArgumentParser(description='Process a Discord CSS file and run a bot.')
    parser.add_argument('css_file', help='Path to the Discord CSS file')

    args = parser.parse_args()

    extract(args.css_file)
    bot.run(token)

if __name__ == '__main__':
    main()
