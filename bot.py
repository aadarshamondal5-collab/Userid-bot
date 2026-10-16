import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8828208168:AAGD_gZBC3GEGlAaE_ttduDnqzyzFS8LNPM"  # get it from @BotFather

bot = Bot(TOKEN)
dp = Dispatcher()


def build_info(message: Message) -> str:
    u = message.from_user
    c = message.chat
    lines = [
        "<b>User info</b>",
        f"User ID: <code>{u.id}</code>",
        f"Chat ID: <code>{c.id}</code>",
        f"Chat type: {c.type}",
        f"First name: {u.first_name}",
        f"Last name: {u.last_name or '-'}",
        f"Username: @{u.username}" if u.username else "Username: -",
        f"Language: {u.language_code or '-'}",
        f"Is bot: {u.is_bot}",
        f"Premium: {bool(u.is_premium)}",
    ]
    if c.title:
        lines.append(f"Chat title: {c.title}")
    return "\n".join(lines)


@dp.message(Command("start", "id", "info"))
async def send_info(message: Message):
    await message.answer(build_info(message), parse_mode="HTML")


# Forwarded messages: show the original sender's ID too
@dp.message(F.forward_origin)
async def forwarded(message: Message):
    origin = message.forward_origin
    sender = getattr(origin, "sender_user", None)
    if sender:
        await message.answer(
            f"Forwarded from: {sender.full_name}\nID: <code>{sender.id}</code>",
            parse_mode="HTML",
        )
    else:
        await message.answer("That user's ID is hidden by their privacy settings.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
