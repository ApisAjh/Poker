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
    "label_turn_notimer": "<b>Giliran</b>\n👤 {name}",
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

    # ----- help / start extras -----
    "help_menu_hint": "\n\n📚 Ketik /tutorial untuk panduan interaktif lengkap.",

    # ----- first-time welcome -----
    "welcome_first": (
        "👋 <b>Selamat Datang di Texas Hold'em!</b>\n\n"
        "Apakah ini pertama kalinya kamu bermain?\n\n"
        "Kami sarankan baca panduan singkat dulu."
    ),
    "welcome_btn_tutorial": "📖 Tutorial",
    "welcome_btn_skip": "▶ Lewati",

    # ----- tutorial menu & nav -----
    "tut_menu": (
        "📚 <b>Panduan Poker</b>\n\n"
        "Pilih topik yang ingin dipelajari.\n"
        "Cocok untuk yang belum pernah main Texas Hold'em."
    ),
    "tut_btn_basics": "📖 Dasar Poker",
    "tut_btn_flow": "🎮 Cara Bermain",
    "tut_btn_examples": "🃏 Contoh Permainan",
    "tut_btn_ranking": "🎴 Ranking Kartu",
    "tut_btn_buttons": "🎯 Arti Tombol",
    "tut_btn_tips": "💡 Tips Bermain",
    "tut_btn_faq": "❓ FAQ",
    "tut_btn_lang": "🌐 Ganti Bahasa",
    "tut_btn_prev": "⬅ Sebelumnya",
    "tut_btn_home": "🏠 Beranda",
    "tut_btn_next": "➡ Berikutnya",

    # ----- tutorial pages -----
    "tut_basics": (
        "📖 <b>Apa Itu Texas Hold'em?</b>\n\n"
        "Texas Hold'em adalah permainan kartu.\n\n"
        "Setiap pemain memperoleh:\n"
        "🃏 <b>2 kartu pribadi</b> (Hole Cards)\n"
        "Hanya kamu yang bisa melihatnya.\n\n"
        "Kemudian bot membuka:\n"
        "🂠🂠🂠🂠🂠\n"
        "<b>5 Community Cards</b>\n"
        "Dipakai bersama semua pemain.\n\n"
        "Tujuan: buat <b>kombinasi 5 kartu terbaik</b> "
        "dari 2 kartu pribadi + 5 community "
        "(total 7 kartu, pilih 5 terbaik)."
    ),
    "tut_flow": (
        "🎮 <b>Alur Permainan</b>\n\n"
        "🎮 Buat Room  (/poker)\n"
        "↓\n"
        "👥 Pemain Join\n"
        "↓\n"
        "▶ Host Memulai Game\n"
        "↓\n"
        "🃏 Semua pemain mendapat 2 kartu\n"
        "<i>Pre-Flop – putuskan Check / Raise / Fold</i>\n"
        "↓\n"
        "🃏 <b>Flop</b> – 3 community cards terbuka\n"
        "↓\n"
        "🃏 <b>Turn</b> – kartu community ke-4\n"
        "↓\n"
        "🃏 <b>River</b> – kartu community ke-5\n"
        "↓\n"
        "🏁 <b>Showdown</b> – semua kartu dibuka\n"
        "↓\n"
        "🏆 <b>Pemenang</b>\n\n"
        "Di setiap tahap, pemain bergiliran menekan tombol aksi."
    ),
    "tut_examples": (
        "🃏 <b>Contoh Permainan</b>\n\n"
        "<b>Contoh 1</b>\n"
        "Community: 2♦ 7♣ J♠ 5♥ K♣\n"
        "Kartu kamu: J♦ 4♠\n"
        "Hasil: ✅ <b>Pair</b> (dua Jack)\n"
        "━━━━━━━━━━━━\n"
        "<b>Contoh 2</b>\n"
        "Community: 8♣ 9♦ 10♠ J♣ 2♥\n"
        "Kartu kamu: Q♦ K♦\n"
        "Hasil: ✅ <b>Straight</b> (8-9-10-J-Q)\n"
        "━━━━━━━━━━━━\n"
        "<b>Contoh 3</b>\n"
        "Community: A♥ A♣ 7♠ 3♦ 2♣\n"
        "Kartu kamu: A♦ K♠\n"
        "Hasil: ✅ <b>Three of a Kind</b> (tiga Ace)\n"
        "━━━━━━━━━━━━\n"
        "<b>Contoh 4</b>\n"
        "Community: K♥ 9♥ 2♥ 5♣ 8♦\n"
        "Kartu kamu: A♥ 3♥\n"
        "Hasil: ✅ <b>Flush</b> (lima hati)"
    ),
    "tut_buttons": (
        "🎯 <b>Arti Tombol</b>\n\n"
        "✅ <b>Check</b>\n"
        "Lewati giliran tanpa menambah taruhan.\n"
        "Pakai jika belum ada yang raise dan kamu ingin tetap murah.\n"
        "━━━━━━━━━━━━\n"
        "📞 <b>Call</b>\n"
        "Ikuti taruhan lawan agar tetap di tangan.\n"
        "━━━━━━━━━━━━\n"
        "⬆ <b>Raise</b>\n"
        "Naikkan taruhan.\n"
        "Biasanya dipakai jika kartumu bagus.\n"
        "━━━━━━━━━━━━\n"
        "❌ <b>Fold</b>\n"
        "Menyerah di ronde ini.\n"
        "Kartu dibuang; kamu tidak bisa menangkan pot.\n"
        "Fold adalah strategi, bukan kegagalan!"
    ),
    "tut_ranking": (
        "🏆 <b>Ranking Kartu</b>\n"
        "<i>Terkuat → terlemah</i>\n\n"
        "🥇 <b>Royal Flush</b>\n"
        "10 J Q K A – satu suit\n"
        "━━━━━━━━━━━━\n"
        "🥈 <b>Straight Flush</b>\n"
        "Lima berurutan, satu suit (contoh 5♥6♥7♥8♥9♥)\n"
        "━━━━━━━━━━━━\n"
        "🥉 <b>Four of a Kind</b>\n"
        "Empat kartu sama (contoh 7♠7♥7♣7♦)\n"
        "━━━━━━━━━━━━\n"
        "4️⃣ <b>Full House</b>\n"
        "Tiga + Pair (contoh K K K + 8 8)\n"
        "━━━━━━━━━━━━\n"
        "5️⃣ <b>Flush</b>\n"
        "Lima satu suit, rank apa saja (♥♥♥♥♥)\n"
        "━━━━━━━━━━━━\n"
        "6️⃣ <b>Straight</b>\n"
        "Lima berurutan (contoh 6 7 8 9 10)\n"
        "━━━━━━━━━━━━\n"
        "7️⃣ <b>Three of a Kind</b>\n"
        "Tiga kartu sama (contoh 7♠7♥7♣)\n"
        "━━━━━━━━━━━━\n"
        "8️⃣ <b>Two Pair</b>\n"
        "Dua pair berbeda\n"
        "━━━━━━━━━━━━\n"
        "9️⃣ <b>Pair</b>\n"
        "Dua kartu sama (contoh A♠ A♦)\n"
        "━━━━━━━━━━━━\n"
        "🔟 <b>High Card</b>\n"
        "Tidak ada kombinasi – kartu tertinggi menang"
    ),
    "tut_tips": (
        "💡 <b>Tips Bermain</b>\n\n"
        "• Pair lebih kuat daripada High Card.\n"
        "• Jangan selalu Raise – pilih-pilih.\n"
        "• Fold adalah strategi pintar, bukan kalah.\n"
        "• Community Cards dipakai semua pemain.\n"
        "• Check saja jika kartu masih jelek.\n"
        "• Sabar lebih baik daripada agresif terus.\n"
        "• Perhatikan kombinasi yang mungkin dari board.\n"
        "• 2 kartu pribadi paling berharga saat nyambung ke board.\n"
        "• Jika hanya satu pemain tersisa (lainnya fold), dia menang otomatis."
    ),
    "tut_faq": (
        "❓ <b>FAQ</b>\n\n"
        "<b>Q: Community Cards milik siapa?</b>\n"
        "A: Tidak milik siapa pun – dipakai bersama semua pemain.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Bagaimana bot menentukan pemenang?</b>\n"
        "A: Bot menghitung kombinasi 5 kartu terbaik dari "
        "2 hole + 5 community, lalu membandingkan ranking.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Kalau kombinasi sama?</b>\n"
        "A: Dibandingkan kicker (kartu samping). Seri murni = split pot.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Kenapa Pair saya kalah?</b>\n"
        "A: Lawan punya kombinasi lebih tinggi "
        "(Two Pair, Straight, Flush, dll.) atau pair lebih tinggi.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Apakah Fold berarti kalah?</b>\n"
        "A: Tidak. Kamu hanya keluar dari ronde ini. Fold untuk hindari kerugian lebih besar.\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Bisa lihat kartu hole lawan?</b>\n"
        "A: Hanya di Showdown (jika mereka tidak fold).\n"
        "━━━━━━━━━━━━\n"
        "<b>Q: Berapa pemain per room?</b>\n"
        "A: Minimal 2, maksimal 6."
    ),
    # ----- game modes -----
    "mode_select_title": "🎮 <b>Pilih Mode Permainan</b>\n\nPilih cara bermain untuk room ini.",
    "mode_classic": "♠ Poker Classic",
    "mode_private": "🃏 Poker Private",
    "mode_classic_desc": "Semua aksi di grup. Cepat & sederhana.",
    "mode_private_desc": "Kartu pribadi hanya lewat Inline Mode. Privasi seperti poker sungguhan.",
    "btn_open_hand": "🎴 Open Hand",
    "private_turn_hint": "👉 {player} — tekan tombol di bawah untuk membuka kartumu.",
    "inline_not_in_game": "❌ Anda tidak sedang bermain.",
    "inline_game_over": "❌ Game telah berakhir.",
    "inline_not_your_turn": "❌ Bukan giliranmu.",
    "inline_title_cards": "{cards}  ·  kartu Anda",
    "inline_desc_check": "Check – lewati tanpa taruhan",
    "inline_desc_call": "Call – ikuti taruhan",
    "inline_desc_raise": "Raise – naikkan taruhan",
    "inline_desc_fold": "Fold – keluar dari ronde",
    "inline_action_posted": "👤 {player}\n{action}",
    "private_help_inline": "Ketik @{bot} di chat ini untuk membuka kartu.",


    "tut_btn_modes": "🎮 Mode Permainan",
    "tut_modes": (
        "🎮 <b>Mode Permainan</b>\n\n"
        "Bot ini punya dua cara bermain.\n\n"
        "━━━━━━━━━━━━\n"
        "♠ <b>Poker Classic</b>\n\n"
        "Mode sederhana.\n"
        "Semua aksi langsung di grup.\n"
        "Saat giliranmu bot menampilkan tombol:\n"
        "✅ Check  📞 Call  ⬆ Raise  ❌ Fold\n\n"
        "Kartu hole tetap tersembunyi (🂠🂠) sampai showdown.\n"
        "Cocok untuk permainan cepat.\n"
        "━━━━━━━━━━━━\n"
        "🃏 <b>Poker Private</b>\n\n"
        "Terinspirasi bot UNO Telegram.\n"
        "Permainan tetap di grup, tapi 2 kartu\n"
        "pribadi hanya terlihat oleh pemiliknya.\n\n"
        "Saat giliranmu tekan:\n"
        "🎴 <b>Open Hand</b>\n\n"
        "Inline Mode Telegram menampilkan kartu <b>hanya milikmu</b>.\n"
        "Pilih Check / Call / Raise / Fold di sana.\n"
        "Grup hanya melihat aksi, bukan kartumu.\n\n"
        "Seperti privasi poker sungguhan."
    )
}
