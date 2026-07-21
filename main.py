import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! سپاس بۆ بەکارهێنانی ئەم بۆتە ❤️\nتکایە لینکی ڤیدیۆکەم بۆ بنێرە تا بۆت دابەزێنم.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("دەستکرا بە پرۆسەی داگرتن... تکایە چاوەڕێ بکە ⏳")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'keepvideo': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            base_filename, _ = os.path.splitext(filename)
            mp3_file = f"{base_filename}.mp3"
            video_file = f"{base_filename}.mp4"

        if os.path.exists(mp3_file):
            await update.message.reply_text("🎵 فایلی دەنگ (Audio):")
            with open(mp3_file, 'rb') as audio:
                await update.message.reply_audio(audio)
            os.remove(mp3_file)

        if os.path.exists(video_file):
            await update.message.reply_text("🎬 فایلی ڤیدیۆ (Video):")
            with open(video_file, 'rb') as video:
                await update.message.reply_video(video)
            os.remove(video_file)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"کێشەیەک ڕوویدا لە کاتی داگرتندا: {str(e)}")

def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("بۆتەکە چالاک کرا و ئامادەی ئیشکردنە...")
    app.run_polling()

if __name__ == '__main__':
    main()
