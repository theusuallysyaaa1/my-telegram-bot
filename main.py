import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سڵاو! لینکی (YouTube, Instagram, TikTok, Facebook) بنێرە:\n\n"
        "🎬 بۆ ڤیدیۆ: ڤیدیۆکەت بۆ دەنێرم.\n"
        "🎵 بۆ MP3: فەرماندەی دەنگ بنێرە یان تەنها لینک بنێرە، دەنگەکەی جیا دەکەمەوە."
    )

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not (url.startswith("http://") or url.startswith("https://")):
        return

    msg = await update.message.reply_text("دەستکرا بە داگرتنی فایلەکە... ⏳")

    # ڕێکخستنی بنەڕەتی بۆ بەزاندنی ئاستەنگەکان
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        },
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    try:
        # ۱. سەرەتا هەوڵ دەدەین ڤیدیۆیەکی پاک داگرین
        video_opts = {
            **ydl_opts,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }

        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # ناردنی ڤیدیۆ ئەگەر هەبوو
        if os.path.exists(filename):
            await update.message.reply_text("🎬 **ڤیدیۆ:**")
            with open(filename, 'rb') as f:
                await update.message.reply_video(f)
            
            # دروستکردنی کۆپییەک بە دەنگی MP3 ڕاستەوخۆ لە ڤیدیۆ داگیراوەکە بێ دووبارە داگرتنەوە!
            base, ext = os.path.splitext(filename)
            mp3_filename = base + ".mp3"
            
            # بەکارهێنانی ffmpeg بۆ وەرگرتنی دەنگ بەبێ داگرتنەوەی لینکەکە
            os.system(f'ffmpeg -y -i "{filename}" -q:a 0 -map a "{mp3_filename}"')

            if os.path.exists(mp3_filename):
                await update.message.reply_text("🎵 **فایلی دەنگی (MP3):**")
                with open(mp3_filename, 'rb') as audio:
                    await update.message.reply_audio(audio)
                os.remove(mp3_filename)

            # سڕینەوەی ڤیدیۆکە لە سێرڤەر
            os.remove(filename)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"کێشەیەک ڕوویدا:\n{str(e)}")

def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("بۆتەکە ئۆنلاینە...")
    app.run_polling()

if __name__ == '__main__':
    main()
