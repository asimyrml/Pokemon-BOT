import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random
# Bot için yetkileri/intents ayarlama
intents = discord.Intents.default()  # Varsayılan ayarların alınması
intents.messages = True              # Botun mesajları işlemesine izin verme
intents.message_content = True       # Botun mesaj içeriğini okumasına izin verme
intents.guilds = True                # Botun sunucularla çalışmasına izin verme

# Tanımlanmış bir komut önekine ve etkinleştirilmiş amaçlara sahip bir bot oluşturma
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot çalışmaya hazır olduğunda tetiklenen bir olay
@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')  # Botun adını konsola çıktı olarak verir

# !go komutu, kullanıcıya rastgele bir Pokémon oluşturur ve bilgilerini gönderir
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Komutu çağıran kullanıcının adını alır
    if author not in Pokemon.pokemons:  # Bu kullanıcı için zaten bir Pokémon olup olmadığını kontrol ederiz
        chance = random.randint(1, 3)  # 1 ile 3 arasında rastgele bir sayı oluştururuz
        # Rastgele sayıya göre bir Pokémon nesnesi oluştururuz
        if chance == 1:
            pokemon = Pokemon(author)  # Standart bir Pokémon oluştururuz
        elif chance == 2:
            pokemon = Wizard(author)  # Wizard türünde bir Pokémon oluştururuz
        elif chance == 3:
            pokemon = Fighter(author)  # Fighter türünde bir Pokémon oluştururuz
        await ctx.send(await pokemon.info())  # Pokémon hakkında bilgi göndeririz
        image_url = await pokemon.show_img()  # Pokémon görüntüsünün URL'sini alırız
        if image_url:
            embed = discord.Embed()  # Gömülü bir mesaj (embed) oluştururuz
            embed.set_image(url=image_url)  # Gömülü mesaja görüntüyü ekleriz
            await ctx.send(embed=embed)  # Görüntülü gömülü mesajı göndeririz
        else:
            await ctx.send("Pokémon görüntüsü yüklenemedi.")  # Görüntü yüklenemezse hata mesajı veririz
    else:
        await ctx.send("Zaten bir Pokémon oluşturmuşsun.")  # Kullanıcıya zaten bir Pokémon oluşturduğunu bildiririz

# !attack komutu
@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  # Mesajda belirtilen kullanıcıyı alırız
    if target:  # Kullanıcının belirtilip belirtilmediğini kontrol ederiz
        # Hem saldırganın hem de hedefin Pokémon sahibi olup olmadığını kontrol ederiz
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]  # Hedefin Pokémon'unu alırız
            attacker = Pokemon.pokemons[ctx.author.name]  # Saldırganın Pokémon'unu alırız
            result = await attacker.attack(enemy)  # Saldırıyı gerçekleştirir ve sonucu alırız
            await ctx.send(result)  # Saldırı sonucunu göndeririz
        else:
            await ctx.send("Savaş için her iki tarafın da Pokémon sahibi olması gerekir!")  # Katılımcılardan birinin Pokémon'u yoksa bilgilendiririz
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")  # Saldırmak için kullanıcıyı etiketleyerek belirtmesini isteriz


@bot.command()
async def info(ctx):
    if ctx.author.name in Pokemon.pokemons:
        pok = Pokemon.pokemons[ctx.author.name]
        await ctx.send(await pok.info())
    else:
        await ctx.send("Henüz bir Pokémon'un yok! '!go' komutunu kullanarak oluşturabilirsin.")


# '!feed' komutu
@bot.command()
async def feed(ctx):
    author = ctx.author.name          # Komutu atan oyuncu
    if author in Pokemon.pokemons:    # Oyuncunun Pokémon’u var mı?
        pokemon = Pokemon.pokemons[author]
        result = await pokemon.feed() # Az önce eklediğimiz feed metodunu çağır
        await ctx.send(result)        # Sonucu kanala gönder
    else:
        await ctx.send("Henüz Pokémon’un yok! '!go' yazarak bir tane yakala.")



# Botun çalıştırılması
bot.run(token)
