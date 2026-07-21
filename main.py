import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! سپاس بۆ بەکارهێنانی ئەم بۆتە ❤️\nتکایە لینکی ڤیدیۆی YouTube یان تۆڕە کۆمەڵایەتییەکانم بۆ بنێرە.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("دەستکرا بە پرۆسەی داگرتن... تکایە چاوەڕێ بکە ⏳")

    try:
        # بەکارهێنانی API بۆ تێپەڕاندنی بلۆکی IPی سێرڤەر
        api_url = f"https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url,
            "vCodec": "h264"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        data = response.json()

        if "url" in data:
            download_link = data["url"]
            video_data = requests.get(download_link).content
            
            file_path = "video.mp4"
            with open(file_path, "wb") as f:
                f.write(video_data)

            await update.message.reply_text("🎬 فایلی ڤیدیۆ (Video):")
            with open(file_path, "rb") as video:
                await update.message.reply_video(video)

            os.remove(file_path)
            await msg.delete()
        else:
            await msg.edit_text("کێشەیەک لە لینکی سەرچاوەدا هەیە یان پشتیوانی ناکرێت.")

    except Exception as e:
        await msg.edit_text(f"کێشەیەک ڕوویدا لە کاتی داگرتندا: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("بۆتەکە چالاک کرا...")
    app.run_polling()

if __name__ == '__main__':
    main()
