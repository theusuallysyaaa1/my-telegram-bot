import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! لینکی یوتیوبەکە بنێرە تا دەنگ و ڤیدیۆکەت بۆ دابەزێنم 🎬🎵")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("دەستکرا بە پرۆسەی داگرتن لە یوتیوب... ⏳")

    # فێڵکردن لە یوتیوب تا وەک مۆبایلی ئاندرۆید سەیرمان بکات و بلۆکمان نەکات
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios']
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.exists(filename):
            await update.message.reply_text("🎬 **ڤیدیۆی یوتیوب:**")
            with open(filename, 'rb') as f:
                await update.message.reply_video(f)
            os.remove(filename)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"کێشەیەک لە داگرتنی یوتیوب هەیە:\n{str(e)}")

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
