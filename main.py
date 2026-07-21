import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! سپاس بۆ هەڵبژاردن و بەکارهێنانی ئەم بۆتە ❤️\nتکایە لینکی ڤیدیۆکەم بۆ بنێرە تا بۆت دابەزێنم.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("دەستکرا بە پرۆسەی داگرتن... تکایە چاوەڕێ بکە ⏳")

    try:
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url
        }

        res = requests.post(api_url, json=payload, headers=headers, timeout=30)
        data = res.json()

        if "url" in data:
            file_url = data["url"]
            video_res = requests.get(file_url, stream=True)
            
            file_path = "downloaded_video.mp4"
            with open(file_path, "wb") as f:
                for chunk in video_res.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            await update.message.reply_text("🎬 فایلی ڤیدیۆ (Video):")
            with open(file_path, "rb") as video:
                await update.message.reply_video(video)

            if os.path.exists(file_path):
                os.remove(file_path)
            await msg.delete()
        else:
            await msg.edit_text("کێشەیەک لە لينکەکەدا هەیە یان سێرڤەرەکە ناتوانێت ئەم ڤیدیۆیە دابەزێنێت.")

    except Exception as e:
        await msg.edit_text(f"کێشەیەک ڕوویدا: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("بۆتەکە چالاک کرا...")
    app.run_polling()

if __name__ == '__main__':
    main()
