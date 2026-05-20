import os
import time
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ⚠️ لێرەدا لە جیاتی ئەم نووسینە، تۆکنی بۆتەکەی خۆت دابنێ ⚠️
TOKEN = 'YOUR_BOT_TOKEN_HERE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"سڵاو {user_name} گیان! 🚀\n\n"
      "من لێرەم بۆ یارمەتیدانی تۆ هاورێی ئەزیز.\n"
        "تەنها لینکی ڤیدیۆکەم بۆ بنێرە (یوتیوب, ئینستاگرام, تیکتۆک...) و منیش بۆتی دەنێرمەوە."
    )

async def handle_video_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_id = update.effective_user.id
    output_filename = f"video_{user_id}_{int(time.time())}.mp4"
    status_message = await update.message.reply_text('⏳ تکایە چاوەڕوان بە... خەریکم ڤیدیۆکە دایدەبەزێنم...')

    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_filename):
            await status_message.edit_text('⚡ دابەزاندن سەرکەوتوو بوو! ئێستا ڤیدیۆکەت بۆ دەنێرم...')
            with open(output_filename, 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="فەرموو ڤیدیۆکەت ئامادەیە! ✨")
            await status_message.delete()
        else:
            await status_message.edit_text('❌ ببوورە، فایلەکە نەدۆزرایەوە.')
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await status_message.edit_text('❌ کێشەیەک ڕوویدا! دڵنیا ببەوە کە لینکەکە گشتییە و کێشەی نییە.')
    finally:
        if os.path.exists(output_filename):
            os.remove(output_filename)

def main():
    while True:
        try:
            logger.info("دەستپێکردنی کارکردنی بۆتەکە...")
            application = Application.builder().token(TOKEN).build()
            application.add_handler(CommandHandler("start", start))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_download))
            application.run_polling(drop_pending_updates=True)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            time.sleep(5)

if __name__ == '__main__':
    main()
