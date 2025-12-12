import subprocess
import sys

def install_modules():
    modules = [
        "nextcord",
        "colorama"
    ]

    for module in modules:
        try:
            __import__(module)
            print(f"{module} ติดตั้งแล้ว")
        except ImportError:
            print(f"{module} กำลังติดตั้งรอ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

install_modules()



import nextcord
from nextcord.ext import commands
import config
import os
from datetime import datetime
import io

bot = commands.Bot(command_prefix="/", intents=nextcord.Intents.all())

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')  # ล้างหน้าจอ
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(Colors.OKCYAN + f"""
╔════════════════════════════════════════════════════╗
║           Jared SHOP V.2 ระบบพร้อมใช้งาน         ║
╠════════════════════════════════════════════════════╣
║  ชื่อบอท       : {bot.user.name:<35}║
║  ไอดีบอท       : {bot.user.id:<35}║
║  เวลา           : {current_time:<35}║
║                                                    ║
║  ลิขสิทธิ์      : icewen_2                         ║
║  Copyright    : © 2025 icewen_2 All Rights Reserved║
╚════════════════════════════════════════════════════╝
""" + Colors.ENDC)

# /// config.py กำหนดในไฟล์นั้น

ownerid = config.ownerid
CHANNEL_ID = config.CHANNEL_ID
emoji1 = config.emoji1
emoji2 = config.emoji2
emoji3 = config.emoji3
emoji4 = config.emoji4


class Product(nextcord.ui.Modal):
    def __init__(self, user: nextcord.User, image: nextcord.Attachment | None):
        super().__init__("กรอกข้อมูลสินค้า")

        self.product_name = nextcord.ui.TextInput(
            label="ชื่อสินค้า", placeholder="เช่น Discord Nitro", required=True, max_length=1000
        )
        self.price = nextcord.ui.TextInput(
            label="ราคา (บาท)", placeholder="เช่น 100", required=True, style=nextcord.TextInputStyle.short
        )
        self.quantity = nextcord.ui.TextInput(
            label="จำนวน", placeholder="เช่น 1", required=True, style=nextcord.TextInputStyle.short
        )

        self.add_item(self.product_name)
        self.add_item(self.price)
        self.add_item(self.quantity)

        self.user = user
        self.image = image

    async def callback(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title=f"{emoji1} : **__JARED ORDER__**",
            description=f"{emoji2} ชื่อสินค้า: ```{self.product_name.value}```\n"
                        f"{emoji3} ราคา: ```{self.price.value} บาท```\n"
                        f"{emoji4} จำนวน: ```{self.quantity.value}```"
        )
        embed.set_footer(text="ICEWEN_2 : ORDER", icon_url="https://cdn.discordapp.com/attachments/1347632960244940841/1357641155478683758/IMG_3789.gif?ex=67f0f15b&is=67ef9fdb&hm=491f6d19ba4ce34e54e76250d7743e94d5ad29165250f16e2473f04026fb9632&")
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)

        if self.image:
            embed.set_image(url="attachment://" + self.image.filename)

        try:
            channel = bot.get_channel(CHANNEL_ID)
            if not channel:
                await interaction.response.send_message("### ❌ ไม่พบช่องที่ระบุ", ephemeral=True)
                return

            if self.image:
                file = await self.image.to_file()
                await channel.send(content=f"{self.user.mention}", embed=embed, file=file)
            else:
                await channel.send(content=f"{self.user.mention}", embed=embed)

            await interaction.response.send_message(" ```ส่งข้อความเรียบร้อยแล้ว```", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"เกิดข้อผิดพลาด: {e}", ephemeral=True)


#/////  คำสั่ง /send เอาไว้ ส่งสินค้านะค้าบ
@bot.slash_command(name="send", description="ส่ง Embed สินค้าไปยังผู้ใช้")
async def send(
    interaction: nextcord.Interaction,
    user: nextcord.User = nextcord.SlashOption(name="user", description="เลือกผู้รับ", required=True),
    image: nextcord.Attachment = nextcord.SlashOption(name="image", description="อัปโหลดรูปสินค้า (ไม่ใส่ก็ได้)", required=False)
):
    if interaction.user.id not in ownerid:
        await interaction.response.send_message("``` เจ้าไม่มีสิทธิ์ใช้คำสั่งนี้ค่ะ```", ephemeral=True)
        return
    modal = Product(user=user, image=image)
    await interaction.response.send_modal(modal)

bot.run(config.TOKEN)