import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سڵاو! لینکی (YouTube, Instagram, TikTok, Facebook) بنێرە، دەستبەجێ ڤیدیۆ و دەنگەکەت بۆ دابەزێنم 🎬🎵"
    )

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not (url.startswith("http://") or url.startswith("https://")):
        return

    msg = await update.message.reply_text("دەستکرا بە پرۆسەی داگرتنی فایدەکە... ⏳")

    # ڕێکخستنی گشتی بۆ هەموو پلاتفۆرمەکان (YouTube, Insta, TikTok, FB)
    ydl_opts_base = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }

    # ۱. داگرتنی ڤیدیۆ
    video_opts = {
        **ydl_opts_base,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s_video.%(ext)s',
        'max_filesize': 50000000, # سنووری ۵۰ مێگابایت بۆ تلیگرام
    }

    # ۲. داگرتنی دەنگ (MP3)
    audio_opts = {
        **ydl_opts_base,
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        # پرۆسەی داگرتن و ناردنی ڤیدیۆ
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info_v = ydl.extract_info(url, download=True)
            v_filename = ydl.prepare_filename(info_v)

        if os.path.exists(v_filename):
            await update.message.reply_text("🎬 **فایلی ڤیدیۆ:**")
            with open(v_filename, 'rb') as video:
                await update.message.reply_video(video)
            os.remove(v_filename)

        # پرۆسەی داگرتن و ناردنی MP3
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info_a = ydl.extract_info(url, download=True)
            a_filename = ydl.prepare_filename(info_a)
            if not a_filename.endswith('.mp3'):
                a_filename = os.path.splitext(a_filename)[0] + '.mp3'

        if os.path.exists(a_filename):
            await update.message.reply_text("🎵 **فایلی دەنگی (MP3):**")
            with open(a_filename, 'rb') as audio:
                await update.message.reply_audio(audio)
            os.remove(a_filename)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"کێشەیەک ڕوویدا لە کاتی داگرتن:\n{str(e)}")

def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("بۆتەکە چالاک کرا و ئۆنلاینە...")
    app.run_polling()

if __name__ == '__main__':
    main()
