import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
import datetime

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(1, 100)  # Pokémon'un can puanı
        self.power = random.randint(1, 10)  # Pokémon'un gücü
        self.last_feed_time = datetime.datetime.min
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def feed(self, feed_interval: int = 20, hp_increase:int = 10 ):
        current_time = datetime.datetime.now()
        delta_time = datetime.timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time :
            self.hp += hp_increase
            self.last_feed_time = current_time 
            return f"Pokémon sağlığı geri yüklenir. Mevcut HP: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz:{current_time + delta_time }"

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve çözümlenmesi
                    return data['forms'][0]['name']  #  Pokémon adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür

    async def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"Pokémonunuzun ismi: {self.name} \n Pokemon HP: {self.hp} \n Pokemon Power {self.power}"  # Pokémon adını içeren dizeyi döndürür

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url
                else:
                    return None
    
class Wizard(Pokemon):
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Düşmanın Wizard veri tipi olup olmadığının kontrol edilmesi (Sihirbaz sınıfının bir örneği midir?) 
            sans = random.randint(1, 5) 
            if sans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"
        
    async def feed(self, feed_interval:int = 20, hp_increase:int = 10 ):
        hp_increase = int(hp_increase * 1.5)  # Sihirbaz Pokémon'unun besleme gücünü artırma
        return await super().feed(feed_interval, hp_increase)

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_guc = random.randint(5, 15)  
        self.guc += super_guc
        sonuc = await super().attack(enemy)  
        self.guc -= super_guc
        return sonuc + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_guc}"

    async def feed(self, feed_interval: int = 20, hp_increase: int = 10):
        # Dövüşçüler için besleme aralığı yarıya düşer
        shorter_interval = max(1, feed_interval // 2)
        return await super().feed(shorter_interval, hp_increase)