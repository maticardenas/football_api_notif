import logging
from datetime import date

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config.notif_config import NotifConfig
from src.emojis import Emojis
from src.team_fixtures_manager import TeamFixturesManager
from src.telegram_bot.bot_commands_handler import NextAndLastMatchCommandHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def echo_test(update: Update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def start(update: Update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{Emojis.WAVING_HAND.value} Hola {update.effective_user.first_name}, soy FootballNotifier bot!\n\n"
        f"{Emojis.JOYSTICK.value} /next_match - Chequeá mis comandos disponibles con este comando ;) \n\n"
        f"{Emojis.GOAT.value} {Emojis.ARGENTINA.value} Vamos Messi!",
    )


async def help(update: Update, context):
    text = (
        f"{Emojis.WAVING_HAND.value}Hola {update.effective_user.first_name}!\n\n"
        f" {Emojis.JOYSTICK.value} Estos son mis comandos disponibles (por ahora):\n\n"
        f"• /next_match <team>: próximo partido del equipo.\n"
        f"• /last_match <team>: último partido jugado del equipo."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def next_match(update: Update, context):
    command_handler = NextAndLastMatchCommandHandler(context.args)
    validated_input = command_handler.validate_command_input()

    if validated_input:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=validated_input
        )
    else:
        team = command_handler.get_managed_team(context.args[0])
        current_season = date.today().year
        team_fixtures_manager = TeamFixturesManager(current_season, team.id)
        text, photo = team_fixtures_manager.get_next_team_fixture_text(
            update.effective_user.first_name
        )
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=text,
            parse_mode="HTML",
        )


async def last_match(update: Update, context):
    command_handler = NextAndLastMatchCommandHandler(context.args)
    validated_input = command_handler.validate_command_input()

    if validated_input:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=validated_input
        )
    else:
        team = command_handler.get_managed_team(context.args[0])
        current_season = date.today().year
        team_fixtures_manager = TeamFixturesManager(current_season, team.id)
        text, photo = team_fixtures_manager.get_last_team_fixture_text(
            update.effective_user.first_name
        )
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=text,
            parse_mode="HTML",
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(NotifConfig.TELEGRAM_TOKEN).build()
    start_handler = CommandHandler("fn_start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo_test)
    next_match_handler = CommandHandler("next_match", next_match)
    last_match_handler = CommandHandler("last_match", last_match)
    help_handler = CommandHandler("help", help)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(next_match_handler)
    application.add_handler(last_match_handler)
    application.add_handler(help_handler)

    application.run_polling()
