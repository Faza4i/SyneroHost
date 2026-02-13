import random
import disnake
from disnake.ext import commands
from disnake import TextInputStyle

LOVE_PHRASES = [
    "Ты делаешь мою жизнь светлее просто тем, что ты есть. Спасибо тебе за это 💖",
    "Я правда благодарен, что мы проводим время вместе. С тобой каждый момент особенный ✨",
    "Этот день стал для меня важным, потому что я встречаю его рядом с тобой 💕",
    "Ты приносишь в мою жизнь спокойствие, тепло и искреннюю радость 🌸",
    "С тобой даже обычные разговоры становятся чем-то ценным и настоящим 💌",
    "Я ценю каждую минуту рядом с тобой. Спасибо, что ты есть в моей жизни 💞",
    "Ты вдохновляешь меня становиться лучше и верить в хорошее 💗",
    "Мне по-настоящему важно то, что мы разделяем вместе 🤍",
    "Рядом с тобой я чувствую себя дома 🫶",
    "Я рад, что именно с тобой могу разделить этот день и свои чувства 💘"
]

LOVE_IMAGES = [
    "https://i.pinimg.com/736x/65/cf/76/65cf7625e8c9f3c2b19a2dff8b6bb6be.jpg",
    "https://i.pinimg.com/736x/19/04/49/190449e9e9dedd549faa58e02022b8fe.jpg",
    "https://i.pinimg.com/736x/78/f4/bc/78f4bc63b422b45fa78348096f2d1c37.jpg",
    "https://i.pinimg.com/736x/39/fc/67/39fc67eb446316b982081af20667ede0.jpg",
    "https://i.pinimg.com/736x/58/91/cb/5891cb1892a3b31b49223f5b082091b9.jpg"
]


class LoveResponseModal(disnake.ui.Modal):
    """Модальное окно для ответа на валентинку"""

    def __init__(self, original_sender: disnake.Member, recipient: disnake.Member):
        self.original_sender = original_sender
        self.recipient = recipient

        components = [
            disnake.ui.TextInput(
                label="Ваше сообщение",
                placeholder="Напишите ответное послание с любовью...",
                custom_id="love_message",
                style=TextInputStyle.paragraph,
                min_length=1,
                max_length=1000,
                required=True
            )
        ]

        super().__init__(
            title=f"Ответ для {original_sender.display_name}",
            components=components,
            custom_id="love_response_modal"
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        """Обработка отправки модального окна"""
        message_text = interaction.text_values["love_message"]

        # Создаем embed для ответной валентинки
        embed = disnake.Embed(
            description=message_text,
            color=0xFF1493,
            timestamp=interaction.created_at
        )

        embed.set_author(
            name=f"💝 Ответная валентинка для {self.original_sender.display_name}",
            icon_url=self.original_sender.display_avatar.url
        )

        embed.set_footer(
            text=f"От {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )

        # Добавляем случайную картинку, если массив не пуст
        if LOVE_IMAGES:
            random_image = random.choice(LOVE_IMAGES)
            embed.set_image(url=random_image)

        # Отправляем ответное сообщение с пингом перед текстом
        await interaction.response.send_message(
            content=f"{self.original_sender.mention}",
            embed=embed
        )


class LoveResponseView(disnake.ui.View):
    """View с кнопкой для ответа на валентинку"""

    def __init__(self, original_sender: disnake.Member, recipient: disnake.Member):
        super().__init__(timeout=None)
        self.original_sender = original_sender
        self.recipient = recipient

    @disnake.ui.button(
        label="Ответить взаимностью",
        style=disnake.ButtonStyle.danger,
        emoji="💝"
    )
    async def respond_button(
            self,
            button: disnake.ui.Button,
            interaction: disnake.Interaction
    ):
        """Обработчик нажатия кнопки ответа"""

        # Проверяем, что кнопку нажал получатель валентинки
        if interaction.user.id != self.recipient.id:
            await interaction.response.send_message(
                "Эта кнопка предназначена только для получателя валентинки! 💔",
                ephemeral=True
            )
            return

        # Открываем модальное окно для ввода текста
        modal = LoveResponseModal(
            original_sender=self.original_sender,
            recipient=self.recipient
        )
        await interaction.response.send_modal(modal)


class LoveCog(commands.Cog):
    """Cog с командой для отправки валентинок"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="love",
        description="Отправить валентинку пользователю"
    )
    async def love(
            self,
            inter: disnake.ApplicationCommandInteraction,
            user: disnake.Member = commands.Param(description="Кому отправить валентинку")
    ):
        """Slash-команда для отправки валентинки"""

        # Проверка: нельзя отправить валентинку самому себе
        if user.id == inter.author.id:
            await inter.response.send_message(
                "Нельзя отправить себе ❤️",
                ephemeral=True
            )
            return

        # Выбираем случайную фразу
        random_phrase = random.choice(LOVE_PHRASES) if LOVE_PHRASES else "Ты особенный! 💕"

        # Создаем улучшенный embed
        embed = disnake.Embed(
            description=random_phrase,
            color=0xFF1493,  # Более яркий розовый
            timestamp=inter.created_at
        )

        # Устанавливаем автора как получателя
        embed.set_author(
            name=f"💌 Валентинка для {user.display_name}",
            icon_url=user.display_avatar.url
        )

        # Добавляем футер с отправителем
        embed.set_footer(
            text=f"От {inter.author.display_name}",
            icon_url=inter.author.display_avatar.url
        )

        # Добавляем случайную картинку
        if LOVE_IMAGES:
            random_image = random.choice(LOVE_IMAGES)
            embed.set_image(url=random_image)

        # Создаем view с кнопкой ответа
        view = LoveResponseView(
            original_sender=inter.author,
            recipient=user
        )

        # Отправляем сообщение: пинг перед фразой
        await inter.response.send_message(
            content=f"{user.mention}",
            embed=embed,
            view=view
        )


def setup(bot: commands.Bot):
    """Функция для загрузки cog"""
    bot.add_cog(LoveCog(bot))