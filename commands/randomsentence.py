from twitchio.ext import commands
import random
import os
import requests
import json

class Randomsentence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ("sentence",)) # Get a random sentence, for whatever purpose
    @commands.cooldown(1, 3, commands.Bucket.user)
    async def randomsentence(self, ctx: commands.Context):
        self.user_langs = self.load_user_langs()
        user_lang = self.user_langs.get(ctx.author.name, "en")
        folder = "data"
        file = f"randomsentence_en.txt"
        path = os.path.join(folder, file)
        if os.path.exists(path):
            if os.access(path, os.R_OK):
                try:
                    with open(path, "r") as f:
                        words = f.readlines()
                except Exception as e:
                    await ctx.channel.send(f"{e}")
                    return
                word = random.choice(words)

                message = f"{word}"

            if user_lang != "en":
                target = message
                langpair = f"en|{user_lang}"
                response = requests.get(f"https://api.mymemory.translated.net/get?q={target}&langpair={langpair}&de=")
                if response.status_code == 200:
                    translated = response.json()["responseData"]["translatedText"]
                    await ctx.reply(translated)
                else:
                    await ctx.reply(f"{response.status_code}")
            else:
                await ctx.reply(message)
            
    def load_user_langs(self):
        try:
            with open('user_langs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {} 

def prepare(bot):
    bot.add_cog(Randomsentence(bot))
