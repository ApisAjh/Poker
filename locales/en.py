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

    # ----- tutorial -----
    "tutorial": (
        "📖 <b>How To Play</b>\n\n"
        "Your goal is to build the best possible poker hand.\n\n"
        "Each player receives:\n"
        "• 2 Hole Cards\n\n"
        "Combine them with:\n"
        "• 5 Community Cards\n\n"
        "<b>Game Flow</b>\n"
        "1. Pre-Flop\n"
        "2. Flop\n"
        "3. Turn\n"
        "4. River\n"
        "5. Showdown\n\n"
        "<b>Buttons</b>\n"
        "✅ <b>Check</b> – Pass without betting.\n"
        "📞 <b>Call</b> – Match the current bet.\n"
        "⬆ <b>Raise</b> – Increase the bet.\n"
        "❌ <b>Fold</b> – Leave the current round.\n\n"
        "<b>Hand Rankings</b> (strongest → weakest)\n"
        "Royal Flush\n"
        "Straight Flush\n"
        "Four of a Kind\n"
        "Full House\n"
        "Flush\n"
        "Straight\n"
        "Three of a Kind\n"
        "Two Pair\n"
        "Pair\n"
        "High Card"
    ),
}
