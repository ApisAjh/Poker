"""English strings."""

TEXTS = {
    # ----- start / help -----
    "start": (
        "🃏 <b>Telegram Poker Bot</b>\n\n"
        "Play Texas Hold'em directly in your group!\n\n"
        "<b>Commands</b>\n"
        "/poker – Create a new room\n"
        "/join – Join current room\n"
        "/leave – Leave room\n"
        "/players – List players\n"
        "/startgame – Start the game (host)\n"
        "/cancel – Cancel room (host)\n"
        "/language – Change language\n"
        "/tutorial – How to play\n"
        "/help – Show this help\n\n"
        "Add me to a group and type /poker to begin."
    ),
    "group_only": "❌ This bot only works in groups. Add me to a group and try again.",

    # ----- language -----
    "language_title": "🌐 <b>Choose Language</b>",
    "language_set_id": "✅ Bahasa diubah ke <b>Indonesia</b>.",
    "language_set_en": "✅ Language set to <b>English</b>.",
    "btn_lang_id": "🇮🇩 Bahasa Indonesia",
    "btn_lang_en": "🇺🇸 English",

    # ----- room / lobby -----
    "room_title": "🎮 <b>Poker Room</b>",
    "room_host": "<b>Host</b>\n👤 {host}",
    "room_players": "<b>Players</b>",
    "room_status_waiting": "<b>Status</b>\nWaiting for players... ({count}/{min})",
    "room_status_ready": "<b>Status</b>\nWaiting for host to start ({count}/{max})",
    "game_already_active": "⚠️ A game is already active in this group. Finish or cancel it first.",
    "no_active_room": "No active room. Use /poker first.",
    "no_room": "No active room.",
    "joined": "✅ {player} joined the game!",
    "already_joined": "You already joined.",
    "room_full": "Room full (max {max}).",
    "game_started_already": "Game already started.",
    "left": "Left the room.",
    "not_in_room": "You are not in this room.",
    "cannot_leave_started": "Cannot leave after the game has started.",
    "host_left": "🏠 Host left. Room cancelled.",
    "room_empty": "Room empty – closed.",
    "room_cancelled": "❌ Room cancelled.",
    "only_host_start": "Only the host can start the game.",
    "only_host_cancel": "Only the host can cancel.",
    "need_players": "Need at least {min} players (currently {count}).",
    "game_started": "🎴 Game started!\nShuffling cards...",
    "players_list": "<b>Players ({count})</b>\n{names}",
    "players_popup": "Players ({count}): {names}",

    # ----- lobby buttons -----
    "btn_join": "➕ Join",
    "btn_leave": "➖ Leave",
    "btn_players": "👥 Players",
    "btn_start": "▶ Start",
    "btn_cancel": "❌ Cancel",

    # ----- in-game -----
    "game_title": "🃏 <b>Texas Hold'em</b>",
    "label_players": "<b>Players</b>",
    "label_community": "<b>Community Cards</b>",
    "label_turn_notimer": "<b>Current Turn</b>\n👤 {name}",
    "label_turn": "<b>Current Turn</b>\n👤 {name} ({seconds}s)",
    "label_street": "<b>Street</b>: {street}",
    "folded": "❌ Folded",
    "btn_check": "✅ Check",
    "btn_call": "📞 Call",
    "btn_raise": "⬆ Raise",
    "btn_fold": "❌ Fold",
    "not_your_turn": "Not your turn.",
    "not_in_progress": "Game is not in progress.",
    "already_folded": "You already folded.",
    "cannot_check": "Cannot check – there is a raise. Call or fold.",
    "unknown_action": "Unknown action.",
    "no_active_game": "No active game.",
    "invalid_action": "Invalid action.",
    "time_expired": "Time expired – auto {action}",
    "action_ok": "{action}!",
    "joined_short": "Joined!",
    "left_short": "Left.",
    "cancelled_short": "Cancelled.",
    "started_short": "Game started!",
    "only_host_short": "Only host can start.",
    "only_host_cancel_short": "Only host can cancel.",
    "need_players_short": "Need ≥{min} players.",
    "no_open_room": "No open room.",
    "unknown_button": "Unknown button.",

    # ----- showdown -----
    "showdown_title": "🏁 <b>SHOWDOWN</b>",
    "label_community_short": "<b>Community</b>",
    "winner_title": "🏆 <b>Winner</b>",
    "combination": "<b>Combination</b>\n{combination}",
    "congrats": "🎉 Congratulations!",
    "split_pot": "🤝 <b>Split Pot</b>",
    "hand_rank_high_card": "High Card",
    "hand_rank_pair": "Pair",
    "hand_rank_two_pair": "Two Pair",
    "hand_rank_three": "Three of a Kind",
    "hand_rank_straight": "Straight",
    "hand_rank_flush": "Flush",
    "hand_rank_full_house": "Full House",
    "hand_rank_four": "Four of a Kind",
    "hand_rank_straight_flush": "Straight Flush",
    "hand_rank_royal": "Royal Flush",

    # ----- streets -----
    "street_waiting": "Waiting",
    "street_preflop": "Pre-Flop",
    "street_flop": "Flop",
    "street_turn": "Turn",
    "street_river": "River",
    "street_showdown": "Showdown",
    "street_finished": "Finished",

    # ----- help / start extras -----
    "help_menu_hint": "\n\n📚 Type /tutorial for the full interactive guide.",

    # ----- first-time welcome -----
    "welcome_first": (
        "👋 <b>Welcome to Texas Hold'em!</b>\n\n"
        "Is this your first time playing?\n\n"
        "We recommend reading the short guide first."
    ),
    "welcome_btn_tutorial": "📖 Tutorial",
    "welcome_btn_skip": "▶ Skip",

    # ----- tutorial menu & nav -----
    "tut_menu": (
        "📚 <b>Poker Guide</b>\n\n"
        "Choose a topic to learn.\n"
        "Perfect if you have never played Texas Hold'em before."
    ),
    "tut_btn_basics": "📖 Poker Basics",
    "tut_btn_flow": "🎮 How to Play",
    "tut_btn_examples": "🃏 Example Hands",
    "tut_btn_ranking": "🎴 Hand Rankings",
    "tut_btn_buttons": "🎯 Button Meanings",
    "tut_btn_tips": "💡 Playing Tips",
    "tut_btn_faq": "❓ FAQ",
    "tut_btn_lang": "🌐 Change Language",
    "tut_btn_prev": "⬅ Previous",
    "tut_btn_home": "🏠 Home",
    "tut_btn_next": "➡ Next",

    # ----- tutorial pages -----
    "tut_basics": (
        "📖 <b>What is Texas Hold'em?</b>\n\n"
        "Texas Hold'em is a card game.\n\n"
        "Each player receives:\n"
        "🃏 <b>2 private cards</b> (Hole Cards)\n"
        "Only you can see them.\n\n"
        "Then the bot reveals:\n"
        "🂠🂠🂠🂠🂠\n"
        "<b>5 Community Cards</b>\n"
        "Shared by everyone.\n\n"
        "Your goal: make the <b>best 5-card combination</b> "
        "using your 2 hole cards + the 5 community cards "
        "(7 cards total, pick the best 5)."
    ),
    "tut_flow": (
        "🎮 <b>Game Flow</b>\n\n"
        "🎮 Create Room  (/poker)\n"
        "↓\n"
        "👥 Players Join\n"
        "↓\n"
        "▶ Host Starts Game\n"
        "↓\n"
        "🃏 Everyone gets 2 hole cards\n"
        "<i>Pre-Flop – decide Check / Raise / Fold</i>\n"
        "↓\n"
        "🃏 <b>Flop</b> – 3 community cards open\n"
        "↓\n"
        "🃏 <b>Turn</b> – 4th community card\n"
        "↓\n"
        "🃏 <b>River</b> – 5th community card\n"
        "↓\n"
        "🏁 <b>Showdown</b> – all cards revealed\n"
        "↓\n"
        "🏆 <b>Winner</b>\n\n"
        "At each street, players take turns using the buttons."
    ),
    "tut_examples": (
        "🃏 <b>Example Hands</b>\n\n"
        "<b>Example 1</b>\n"
        "Community: 2♦ 7♣ J♠ 5♥ K♣\n"
        "Your cards: J♦ 4♠\n"
        "Result: ✅ <b>Pair</b> (two Jacks)\n"
        "━━━━━━━━━━━━\n"
        "<b>Example 2</b>\n"
        "Community: 8♣ 9♦ 10♠ J♣ 2♥\n"
        "Your cards: Q♦ K♦\n"
        "Result: ✅ <b>Straight</b> (8-9-10-J-Q)\n"
        "━━━━━━━━━━━━\n"
        "<b>Example 3</b>\n"
        "Community: A♥ A♣ 7♠ 3♦ 2♣\n"
        "Your cards: A♦ K♠\n"
        "Result: ✅ <b>Three of a Kind</b> (three Aces)\n"
        "━━━━━━━━━━━━\n"
        "<b>Example 4</b>\n"
        "Community: K♥ 9♥ 2♥ 5♣ 8♦\n"
        "Your cards: A♥ 3♥\n"
        "Result: ✅ <b>Flush</b> (five hearts)"
    ),
    "tut_buttons": (
        "🎯 <b>Button Meanings</b>\n\n"
        "✅ <b>Check</b>\n"
        "Pass your turn without betting.\n"
        "Use when no one has raised yet and you want to stay in cheaply.\n"
        "━━━━━━━━━━━━\n"
        "📞 <b>Call</b>\n"
        "Match the current bet to stay in the hand.\n"
        "━━━━━━━━━━━━\n"
        "⬆ <b>Raise</b>\n"
        "Increase the bet.\n"
        "Use when your hand looks strong.\n"
        "━━━━━━━━━━━━\n"
        "❌ <b>Fold</b>\n"
        "Give up this round.\n"
        "Your cards are discarded; you cannot win the pot.\n"
        "Fold is a strategy, not a failure!"
    ),
    "tut_ranking": (
        "🏆 <b>Hand Rankings</b>\n"
        "<i>Strongest → weakest</i>\n\n"
        "🥇 <b>Royal Flush</b>\n"
        "10 J Q K A – same suit\n"
        "━━━━━━━━━━━━\n"
        "🥈 <b>Straight Flush</b>\n"
        "Five in a row, same suit (e.g. 5♥6♥7♥8♥9♥)\n"
        "━━━━━━━━━━━━\n"
        "🥉 <b>Four of a Kind</b>\n"
        "Four same rank (e.g. 7♠7♥7♣7♦)\n"
        "━━━━━━━━━━━━\n"
        "4️⃣ <b>Full House</b>\n"
        "Three + Pair (e.g. K K K + 8 8)\n"
        "━━━━━━━━━━━━\n"
        "5️⃣ <b>Flush</b>\n"
        "Five same suit, any ranks (♥♥♥♥♥)\n"
        "━━━━━━━━━━━━\n"
        "6️⃣ <b>Straight</b>\n"
        "Five in a row (e.g. 6 7 8 9 10)\n"
        "━━━━━━━━━━━━\n"
        "7️⃣ <b>Three of a Kind</b>\n"
        "Three same rank (e.g. 7♠7♥7♣)\n"
        "━━━━━━━━━━━━\n"
        "8️⃣ <b>Two Pair</b>\n"
        "Two different pairs\n"
        "━━━━━━━━━━━━\n"
        "9️⃣ <b>Pair</b>\n"
        "Two same rank (e.g. A♠ A♦)\n"
        "━━━━━━━━━━━━\n"
        "🔟 <b>High Card</b>\n"
        "Nothing special – highest card wins"
    ),
    "tut_tips": (
        "💡 <b>Playing Tips</b>\n\n"
        "• A Pair is stronger than High Card.\n"
        "• Don't Raise every hand – be selective.\n"
        "• Folding is smart strategy, not losing.\n"
        "• Community cards are shared by everyone.\n"
        "• Check is fine when your cards are weak.\n"
        "• Patience beats constant aggression.\n"
        "• Watch what combinations the board allows.\n"
        "• Your 2 hole cards matter most when they connect with the board.\n"
        "• If only one player remains (others folded), they win automatically."
    ),
    "tut_faq": (
        "❓ <b>FAQ</b>\n\n"
        "<b>Q: Who owns the Community Cards?</b>\n"
        "A: Nobody – they are shared by all players.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: How does the bot pick a winner?</b>\n"
        "A: It finds each player's best 5-card hand from "
        "2 hole + 5 community cards, then compares rankings.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: What if two players have the same combination?</b>\n"
        "A: Kickers (side cards) decide. True ties split the pot.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Why did my Pair lose?</b>\n"
        "A: The opponent had a higher ranking hand "
        "(Two Pair, Straight, Flush, etc.) or a higher pair.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Does Fold mean I lost the game?</b>\n"
        "A: No. You only leave this round. Fold to avoid bigger losses.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Can I see other players' hole cards?</b>\n"
        "A: Only at Showdown (if they didn't fold).\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: How many players per room?</b>\n"
        "A: Minimum 2, maximum 6."
    ),

    # ----- timeouts -----
    "room_timeout": (
        "⏰ <b>Room closed.</b>\n\n"
        "Not enough players to start within 10 minutes.\n"
        "Use /poker to create a new room."
    ),
    "afk_warning": (
        "⚠️ <b>5 minutes left!</b>\n\n"
        "👤 {player}\n"
        "Take an action before the bot auto-Folds."
    ),
    "afk_fold": (
        "⏰ <b>Time's up!</b>\n\n"
        "👤 {player}\n"
        "marked AFK.\n"
        "Bot auto-Folded. Turn passes to the next player."
    ),


    # ----- game modes -----
    "mode_select_title": "🎮 <b>Choose Game Mode</b>\n\nPick how you want to play this room.",
    "mode_classic": "♠ Poker Classic",
    "mode_private": "🃏 Poker Private",
    "mode_classic_desc": "All actions in the group. Fast & simple.",
    "mode_private_desc": "Hole cards only via Inline Mode. Real poker privacy.",
    "btn_open_hand": "🎴 Open Hand",
    "private_turn_hint": "👉 {player} — press the button below to open your hand.",
    "inline_not_in_game": "❌ You are not in an active game.",
    "inline_game_over": "❌ The game has ended.",
    "inline_not_your_turn": "❌ Not your turn.",
    "inline_title_cards": "{cards}  ·  your hole cards",
    "inline_desc_check": "Check – pass without betting",
    "inline_desc_call": "Call – match the bet",
    "inline_desc_raise": "Raise – increase the bet",
    "inline_desc_fold": "Fold – leave this round",
    "inline_action_posted": "👤 {player}\n{action}",
    "private_help_inline": "Type @{bot} in this chat to open your cards.",


    "tut_btn_modes": "🎮 Game Modes",
    "tut_modes": (
        "🎮 <b>Game Modes</b>\n\n"
        "This bot has two ways to play.\n\n"
        "━━━━━━━━━━━━\n"
        "♠ <b>Poker Classic</b>\n\n"
        "Simple mode.\n"
        "Everything happens in the group.\n"
        "On your turn the bot shows action buttons:\n"
        "✅ Check  📞 Call  ⬆ Raise  ❌ Fold\n\n"
        "Hole cards stay hidden (🂠🂠) until showdown.\n"
        "Best for quick games.\n"
        "━━━━━━━━━━━━\n"
        "🃏 <b>Poker Private</b>\n\n"
        "Inspired by UNO Telegram bots.\n"
        "Play still happens in the group, but your\n"
        "2 hole cards are private.\n\n"
        "On your turn press:\n"
        "🎴 <b>Open Hand</b>\n\n"
        "Telegram Inline Mode shows <b>only your</b> cards.\n"
        "Pick Check / Call / Raise / Fold there.\n"
        "The group only sees your action, never your cards.\n\n"
        "Feels like real poker privacy."
    )
}
