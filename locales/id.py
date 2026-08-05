"""Bahasa Indonesia strings."""

TEXTS = {
    # ----- start / help -----
    "start": (
        "🃏 <b>Telegram Poker Bot</b>\n\n"
        "Main Texas Hold'em langsung di grup!\n\n"
        "<b>Perintah</b>\n"
        "/poker – Buat room baru\n"
        "/join – Gabung room\n"
        "/leave – Keluar dari room\n"
        "/players – Daftar pemain\n"
        "/startgame – Mulai permainan (host)\n"
        "/cancel – Batalkan room (host)\n"
        "/language – Ganti bahasa\n"
        "/tutorial – Cara bermain\n"
        "/help – Tampilkan bantuan\n\n"
        "Tambahkan bot ke grup lalu ketik /poker untuk mulai."
    ),
    "group_only": "❌ Bot ini hanya bisa dipakai di grup. Tambahkan ke grup lalu coba lagi.",

    # ----- language -----
    "language_title": "🌐 <b>Pilih Bahasa</b>",
    "language_set_id": "✅ Bahasa diubah ke <b>Indonesia</b>.",
    "language_set_en": "✅ Language set to <b>English</b>.",
    "btn_lang_id": "🇮🇩 Bahasa Indonesia",
    "btn_lang_en": "🇺🇸 English",

    # ----- room / lobby -----
    "room_title": "🎮 <b>Room Poker</b>",
    "room_host": "<b>Host</b>\n👤 {host}",
    "room_players": "<b>Pemain</b>",
    "room_status_waiting": "<b>Status</b>\nMenunggu pemain... ({count}/{min})",
    "room_status_ready": "<b>Status</b>\nMenunggu host memulai ({count}/{max})",
    "game_already_active": "⚠️ Sudah ada game aktif di grup ini. Selesaikan atau batalkan dulu.",
    "no_active_room": "Tidak ada room aktif. Gunakan /poker dulu.",
    "no_room": "Tidak ada room aktif.",
    "joined": "✅ {player} berhasil bergabung!",
    "already_joined": "Kamu sudah bergabung.",
    "room_full": "Room penuh (maks {max}).",
    "game_started_already": "Permainan sudah dimulai.",
    "left": "Keluar dari room.",
    "not_in_room": "Kamu tidak ada di room ini.",
    "cannot_leave_started": "Tidak bisa keluar setelah permainan dimulai.",
    "host_left": "🏠 Host keluar. Room dibatalkan.",
    "room_empty": "Room kosong – ditutup.",
    "room_cancelled": "❌ Room dibatalkan.",
    "only_host_start": "Hanya host yang bisa memulai permainan.",
    "only_host_cancel": "Hanya host yang bisa membatalkan.",
    "need_players": "Minimal {min} pemain (saat ini {count}).",
    "game_started": "🎴 Permainan dimulai!\nBot sedang mengocok kartu...",
    "players_list": "<b>Pemain ({count})</b>\n{names}",
    "players_popup": "Pemain ({count}): {names}",

    # ----- lobby buttons -----
    "btn_join": "➕ Gabung",
    "btn_leave": "➖ Keluar",
    "btn_players": "👥 Pemain",
    "btn_start": "▶ Mulai",
    "btn_cancel": "❌ Batal",

    # ----- in-game -----
    "game_title": "🃏 <b>Texas Hold'em</b>",
    "label_players": "<b>Pemain</b>",
    "label_community": "<b>Community Cards</b>",
    "label_turn": "<b>Giliran</b>\n👤 {name} ({seconds}s)",
    "label_street": "<b>Tahap</b>: {street}",
    "folded": "❌ Fold",
    "btn_check": "✅ Check",
    "btn_call": "📞 Call",
    "btn_raise": "⬆ Raise",
    "btn_fold": "❌ Fold",
    "not_your_turn": "Bukan giliranmu.",
    "not_in_progress": "Permainan belum berlangsung.",
    "already_folded": "Kamu sudah fold.",
    "cannot_check": "Tidak bisa check – ada raise. Call atau fold.",
    "unknown_action": "Aksi tidak dikenal.",
    "no_active_game": "Tidak ada game aktif.",
    "invalid_action": "Aksi tidak valid.",
    "time_expired": "Waktu habis – otomatis {action}",
    "action_ok": "{action}!",
    "joined_short": "Bergabung!",
    "left_short": "Keluar.",
    "cancelled_short": "Dibatalkan.",
    "started_short": "Permainan dimulai!",
    "only_host_short": "Hanya host yang bisa memulai.",
    "only_host_cancel_short": "Hanya host yang bisa membatalkan.",
    "need_players_short": "Minimal ≥{min} pemain.",
    "no_open_room": "Tidak ada room terbuka.",
    "unknown_button": "Tombol tidak dikenal.",

    # ----- showdown -----
    "showdown_title": "🏁 <b>SHOWDOWN</b>",
    "label_community_short": "<b>Community</b>",
    "winner_title": "🏆 <b>Pemenang</b>",
    "combination": "<b>Kombinasi</b>\n{combination}",
    "congrats": "🎉 Selamat!",
    "split_pot": "🤝 <b>Hasil Seri</b>",
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
    "street_waiting": "Menunggu",
    "street_preflop": "Pre-Flop",
    "street_flop": "Flop",
    "street_turn": "Turn",
    "street_river": "River",
    "street_showdown": "Showdown",
    "street_finished": "Selesai",

    # ----- tutorial -----
    "tutorial": (
        "📖 <b>Cara Bermain</b>\n\n"
        "Tujuan permainan adalah membuat kombinasi kartu terbaik.\n\n"
        "Setiap pemain mendapat:\n"
        "• 2 kartu pribadi (Hole Cards)\n\n"
        "Gabungkan dengan:\n"
        "• 5 Community Cards\n\n"
        "<b>Tahapan Permainan</b>\n"
        "1. Pre-Flop\n"
        "2. Flop\n"
        "3. Turn\n"
        "4. River\n"
        "5. Showdown\n\n"
        "<b>Arti Tombol</b>\n"
        "✅ <b>Check</b> – Tidak menambah taruhan.\n"
        "📞 <b>Call</b> – Mengikuti taruhan.\n"
        "⬆ <b>Raise</b> – Menambah taruhan.\n"
        "❌ <b>Fold</b> – Menyerah.\n\n"
        "<b>Ranking</b> (terkuat → terlemah)\n"
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
