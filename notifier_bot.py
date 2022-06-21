from datetime import date

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from config.notif_config import NotifConfig
from src.emojis import Emojis
from src.notifier_logger import get_logger
from src.team_fixtures_manager import TeamFixturesManager
from src.telegram_bot.bot_commands_handler import (
    NextAndLastMatchCommandHandler,
    NotifierBotCommandsHandler,
)
from src.telegram_bot.bot_constants import MESSI_PHOTO

logger = get_logger(__name__)


async def start(update: Update, context):
    logger.info(f"'start' command executed - by {update.effective_user.name}")
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=MESSI_PHOTO,
        caption=f"{Emojis.WAVING_HAND.value} Hola {update.effective_user.first_name}, soy FootballNotifier bot!\n\n"
        f"{Emojis.JOYSTICK.value} /help - Chequeá mis comandos disponibles ;) \n\n"
        f"{Emojis.GOAT.value} {Emojis.ARGENTINA.value} Vamos Messi!",
        parse_mode="HTML",
    )


async def help(update: Update, context):
    logger.info(f"'help' command executed - by {update.effective_user.name}")
    text = (
        f"{Emojis.WAVING_HAND.value}Hola {update.effective_user.first_name}!\n\n"
        f" {Emojis.JOYSTICK.value} Estos son mis comandos disponibles (por ahora):\n\n"
        f"• /next_match <team>: próximo partido del equipo.\n"
        f"• /last_match <team>: último partido jugado del equipo.\n"
        f"• /available_teams: equipos disponibles.\n"
        f"• /today_matches: partidos de hoy (de los equipos disponibles).\n"
        f"• /tomorrow_matches: partidos de mañana (de los equipos disponibles).\n"
        f"• /last_played_matches: partidos jugados el día de ayer (de los equipos disponibles)."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def available_teams(update: Update, context):
    logger.info(f"'available_teams' command executed - by {update.effective_user.name}")
    notifier_commands_handler = NotifierBotCommandsHandler()
    text = (
        f"{Emojis.WAVING_HAND.value}Hola {update.effective_user.first_name}!\n\n"
        f" {Emojis.TELEVISION.value} Estos son los equipos disponibles:\n\n"
        f"{notifier_commands_handler.available_teams_text()}"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def next_match(update: Update, context):
    logger.info(
        f"'next_match {' '.join(context.args)}' command executed - by {update.effective_user.name}"
    )
    command_handler = NextAndLastMatchCommandHandler(context.args)
    validated_input = command_handler.validate_command_input()

    if validated_input:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=validated_input
        )
    else:
        team_name = context.args[0].lower()
        team = command_handler.get_managed_team(team_name)
        current_season = date.today().year
        team_fixtures_manager = TeamFixturesManager(current_season, team.id)
        text, photo = team_fixtures_manager.get_next_team_fixture_text(
            update.effective_user.first_name
        )
        logger.info(f"Fixture - text: {text} - photo: {photo}")
        if photo:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=text,
                parse_mode="HTML",
            )
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def last_match(update: Update, context):
    logger.info(
        f"'last_match {' '.join(context.args)}' command executed - by {update.effective_user.name}"
    )
    command_handler = NextAndLastMatchCommandHandler(context.args)
    validated_input = command_handler.validate_command_input()

    if validated_input:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=validated_input
        )
    else:
        team_name = context.args[0].lower()
        team = command_handler.get_managed_team(team_name)
        current_season = date.today().year
        team_fixtures_manager = TeamFixturesManager(current_season, team.id)
        text, photo = team_fixtures_manager.get_last_team_fixture_text(
            update.effective_user.first_name
        )
        logger.info(f"Fixture - text: {text} - photo: {photo}")
        if photo:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=text,
                parse_mode="HTML",
            )
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def today_matches(update: Update, context):
    logger.info(
        f"'today_matches {' '.join(context.args)}' command executed - by {update.effective_user.name}"
    )
    command_handler = NotifierBotCommandsHandler()
    text, photo = command_handler.today_games(update.effective_user.first_name)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo,
        caption=text,
        parse_mode="HTML",
    )


async def last_played_matches(update: Update, context):
    logger.info(
        f"'last_played_matches {' '.join(context.args)}' command executed - by {update.effective_user.name}"
    )
    command_handler = NotifierBotCommandsHandler()
    text, photo = command_handler.yesterday_games(update.effective_user.first_name)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo,
        caption=text,
        parse_mode="HTML",
    )


async def tomorrow_matches(update: Update, context):
    logger.info(
        f"'tomorrow_matches {' '.join(context.args)}' command executed - by {update.effective_user.name}"
    )
    command_handler = NotifierBotCommandsHandler()
    text, photo = command_handler.tomorrow_games(update.effective_user.first_name)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo,
        caption=text,
        parse_mode="HTML",
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(NotifConfig.TELEGRAM_TOKEN).build()
    start_handler = CommandHandler("start", start)
    next_match_handler = CommandHandler("next_match", next_match)
    last_match_handler = CommandHandler("last_match", last_match)
    today_matches_handler = CommandHandler("today_matches", today_matches)
    tomorrow_matches_handler = CommandHandler("tomorrow_matches", tomorrow_matches)
    last_played_matches_handler = CommandHandler(
        "last_played_matches", last_played_matches
    )
    available_teams_handler = CommandHandler("available_teams", available_teams)
    help_handler = CommandHandler("help", help)
    application.add_handler(start_handler)
    application.add_handler(next_match_handler)
    application.add_handler(last_match_handler)
    application.add_handler(help_handler)
    application.add_handler(today_matches_handler)
    application.add_handler(last_played_matches_handler)
    application.add_handler(available_teams_handler)
    application.add_handler(tomorrow_matches_handler)

    application.run_polling()
