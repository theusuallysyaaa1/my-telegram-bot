import os
import subprocess
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! لینکی (YouTube, Instagram, TikTok, Facebook) بنێرە تا MP4 و MP3ەکەی بە یەکەوە بۆ دابەزێنم 🎬🎵")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if not (url.startswith("http://") or url.startswith("https://")):
        return

    msg = await update.message.reply_text("دەستکرا بە داگرتنی ڤیدیۆ و دروستکردنی MP3... ⏳")

    # ڕێکخستنی داگرتنی ڤیدیۆکە
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    video_file = None
    mp3_file = None

    try:
        # ١. داگرتنی ڤیدیۆکە (MP4)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)

        # ٢. ناردنی فایلی ڤیدیۆ (MP4)
        if video_file and os.path.exists(video_file):
            await update.message.reply_text("🎬 **فایلی ڤیدیۆ (MP4):**")
            with open(video_file, 'rb') as f_vid:
                await update.message.reply_video(f_vid)

            # ٣. جیاکردنەوەی دەنگەکەی و دروستکردنی فایلی MP3 بە FFmpeg
            mp3_file = os.path.splitext(video_file)[0] + ".mp3"
            cmd = f'ffmpeg -y -i "{video_file}" -vn -ar 44100 -ac 2 -b:a 192k "{mp3_file}"'
            subprocess.run(cmd, shell=True, check=True)

            # ٤. ناردنی فایلی دەنگ (MP3)
            if os.path.exists(mp3_file):
                await update.message.reply_text("🎵 **فایلی دەنگی (MP3):**")
                with open(mp3_file, 'rb') as f_aud:
                    await update.message.reply_audio(f_aud)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"کێشەیەک ڕوویدا لە داگرتن یان دروستکردنی MP3:\n{str(e)}")

    finally:
        # پاککردنەوەی فایلەکان لەسەر سێرڤەر
        if video_file and os.path.exists(video_file):
            os.remove(video_file)
        if mp3_file and os.path.exists(mp3_file):
            os.remove(mp3_file)

def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("بۆتەکە چالاک کرا...")
    app.run_polling()

if __name__ == '__main__':
    main()
