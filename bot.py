import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# --- MASUKKAN DATA ANDA DI SINI ---
API_ID = 32811628                    # Ganti dengan angka API ID Anda
API_HASH = "83c821a443a0808bdfff4619d24c51a3"     # Ganti dengan API HASH Anda
BOT_TOKEN = "9130902719:AAEt4bJAk-F4sEq9xaKpJ6ToJfOdLVlKhOg"    # Ganti dengan Token dari @BotFather

# ID Grup Telegram Anda (berawalan angka minus, contoh: -100xxxxxxxxxx)
TARGET_GROUP_ID = -1004357923040 

# ID Topik "TOBK & Racing" yang ada di grup Anda
TOBK_TOPIC_ID = 2 

app = Client(
    "topic_moderator_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.chat(TARGET_GROUP_ID) & filters.group)
async def check_message_topic(client: Client, message: Message):
    # Abaikan pesan dari bot itu sendiri
    if message.from_user and message.from_user.is_bot:
        return

    # Pastikan pesan berupa teks
    if not message.text:
        return

    target_text = "mohon diisi data kepesertaannya"
    
    # Cek jika pesan mengandung kalimat spesifik tersebut
    if target_text in message.text.lower():
        
        # Ambil ID topik tempat pesan ini dikirim
        current_thread_id = message.message_thread_id
        
        # JIKA DIKIRIM DI TOPIK YANG BENAR (TOBK & Racing), BOT DIAM
        if current_thread_id == TOBK_TOPIC_ID:
            return
        
        # JIKA DIKIRIM DI LUAR TOPIK TERSEBUT (SALAH KAMAR), TEGUR & HAPUS
        warning_msg = await message.reply_text(
            f"⚠️ Maaf {message.from_user.mention}, pesan anda salah kamar, silakan kirim di topik **TOBK & Racing**.\n\n"
            f"*(Pesan ini & peringatan ini akan otomatis dihapus dalam 2 menit)*"
        )
        
        # Tunggu selama 2 menit (120 detik)
        await asyncio.sleep(120)
        
        # Hapus pesan asli anggota dan pesan peringatan bot
        try:
            await message.delete()
            await warning_msg.delete()
        except Exception as e:
            print(f"Gagal menghapus pesan (pastikan bot sudah jadi Admin): {e}")

if __name__ == "__main__":
    print("🤖 Bot moderasi topik sedang berjalan...")
    app.run()