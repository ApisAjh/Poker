"""
Vercel Serverless entry point for Telegram Poker Bot.

Uses FastAPI + python-telegram-bot (webhook mode).
All game state lives in process RAM (games dict).
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)

from bot.handlers import (
    callback_handler,
    cmd_cancel,
    cmd_help,
    cmd_join,
    cmd_language,
    cmd_leave,
    cmd_players,
    cmd_poker,
    cmd_start,
    cmd_startgame,
    cmd_tutorial,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TOKEN") or ""
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")  # e.g. https://xxx.vercel.app

if not TOKEN:
    logger.warning("BOT_TOKEN environment variable is not set!")

# Build PTB application (no updater – we feed updates manually)
ptb = (
    Application.builder()
    .token(TOKEN)
    .updater(None)
    .build()
)

# Register handlers
ptb.add_handler(CommandHandler("start", cmd_start))
ptb.add_handler(CommandHandler("help", cmd_help))
ptb.add_handler(CommandHandler("tutorial", cmd_tutorial))
ptb.add_handler(CommandHandler("language", cmd_language))
ptb.add_handler(CommandHandler("poker", cmd_poker))
ptb.add_handler(CommandHandler("join", cmd_join))
ptb.add_handler(CommandHandler("leave", cmd_leave))
ptb.add_handler(CommandHandler("players", cmd_players))
ptb.add_handler(CommandHandler("startgame", cmd_startgame))
ptb.add_handler(CommandHandler("cancel", cmd_cancel))
ptb.add_handler(CallbackQueryHandler(callback_handler))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start/stop PTB and optionally set webhook on cold start."""
    async with ptb:
        await ptb.start()
        if WEBHOOK_URL:
            try:
                await ptb.bot.set_webhook(
                    url=WEBHOOK_URL.rstrip("/") + "/",
                    allowed_updates=["message", "callback_query"],
                    drop_pending_updates=True,
                )
                logger.info("Webhook set to %s", WEBHOOK_URL)
            except Exception as e:
                logger.error("Failed to set webhook: %s", e)
        yield
        await ptb.stop()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)


@app.get("/")
async def health() -> dict:
    return {"status": "ok", "bot": "poker"}


@app.post("/")
@app.post("/webhook")
async def telegram_webhook(request: Request) -> Response:
    """Receive Telegram updates and process them."""
    try:
        data = await request.json()
        update = Update.de_json(data, ptb.bot)
        await ptb.process_update(update)
    except Exception as e:
        logger.exception("Error processing update: %s", e)
    return Response(status_code=HTTPStatus.OK)


# Local development helper
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
