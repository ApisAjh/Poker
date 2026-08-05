# Telegram Poker Bot (UNO-style • Group Only)

A lightweight multiplayer **Texas Hold'em** bot for Telegram groups.

- 100 % played inside the group (no DM, no Web App)
- No database – all state lives in RAM (`games = {}`)
- Ready for **Vercel Serverless** + Telegram Webhook
- Python 3.12+, `python-telegram-bot` v22, FastAPI

---

## Features

| Feature | Detail |
|---------|--------|
| Players | 2 – 6 |
| One game per group | Yes |
| Hole cards | Hidden (only shown at showdown) |
| Community cards | Revealed step-by-step (Flop → Turn → River) |
| Actions | Check / Call / Raise / Fold (inline buttons) |
| Turn timer | 20 seconds (auto Check or Fold) |
| Hand ranking | Full poker ranking incl. Royal Flush |
| Clean chat | Bot edits **one** status message |

---

## Commands

| Command | Description |
|---------|-------------|
| `/start` `/help` | Help text |
| `/poker` | Create a new room (host) |
| `/join` | Join room |
| `/leave` | Leave room |
| `/players` | List players |
| `/startgame` | Start game (host only) |
| `/cancel` | Cancel room (host only) |

All actions also available via **inline keyboard**.

---

## Project Structure

```
├── api/
│   └── index.py          # Vercel / FastAPI entry point
├── bot/
│   ├── handlers.py       # Commands + callback handlers
│   └── keyboards.py      # Inline keyboards
├── game/
│   ├── cards.py          # Card & Deck
│   ├── evaluator.py      # Pure-Python hand evaluator
│   └── poker.py          # Game state machine
├── requirements.txt
├── vercel.json
└── README.md
```

---

## Local Development

```bash
# 1. Clone / copy the project
cd telegram-poker-bot

# 2. Create virtualenv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install deps
pip install -r requirements.txt

# 4. Set token
export BOT_TOKEN="123456:ABC-DEF..."

# 5. Run locally (for testing with ngrok)
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
```

Expose with ngrok:

```bash
ngrok http 8000
# Then set webhook:
curl "https://api.telegram.org/bot$BOT_TOKEN/setWebhook?url=https://xxxx.ngrok.io/"
```

---

## Deploy to Vercel

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Telegram Poker Bot"
git remote add origin https://github.com/YOUR_USER/telegram-poker-bot.git
git push -u origin main
```

### 2. Import on Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import the repository
3. Framework Preset: **Other**
4. Add Environment Variables:

| Name | Value |
|------|-------|
| `BOT_TOKEN` | Your bot token from @BotFather |
| `WEBHOOK_URL` | `https://your-project.vercel.app` (fill after first deploy) |

5. Deploy

### 3. Set Webhook

After the first deploy you get a URL like `https://telegram-poker-bot-xxx.vercel.app`.

```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://telegram-poker-bot-xxx.vercel.app/"
```

Or set the `WEBHOOK_URL` env var and redeploy – the app will call `setWebhook` on cold start.

### 4. Verify

```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"
```

You should see your Vercel URL.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ | Token from @BotFather |
| `WEBHOOK_URL` | Recommended | Full public URL of the deployment (used to auto-set webhook) |

---

## How the Game Works

1. Someone types `/poker` → room created, host is first player.
2. Others press **➕ Join** (or `/join`).
3. Host presses **▶ Start Game**.
4. Bot deals 2 hole cards (hidden) and shows the status message.
5. Players take turns with **Check / Call / Raise / Fold**.
6. After each street the community cards are revealed by editing the same message.
7. At showdown all hole cards are revealed, winner is calculated, game is deleted from RAM.
8. Group can start a new game immediately with `/poker`.

---

## Important Notes (Serverless)

- **In-memory only** – when the Vercel function cold-starts, the `games` dict is empty. Active games are lost on cold start / scale-to-zero. This is intentional (no DB).
- For longer-lived games consider a single always-on instance (Railway, Render, Fly.io, etc.) instead of pure serverless.
- Turn timer is checked on the next callback (no background threads / schedulers).

---

## Hand Ranking

1. High Card  
2. Pair  
3. Two Pair  
4. Three of a Kind  
5. Straight  
6. Flush  
7. Full House  
8. Four of a Kind  
9. Straight Flush  
10. Royal Flush  

Ties are broken by kicker cards automatically.

---

## License

MIT – free to use and modify.
