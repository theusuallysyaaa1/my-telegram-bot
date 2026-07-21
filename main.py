import os
import requests
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! سپاس بۆ هەڵبژاردن و بەکارهێنانی ئەم بۆتە ❤️\nتکایە لینکی ڤیدیۆکەم بۆ بنێرە.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("دەستکرا بە پرۆسەی داگرتن... تکایە چاوەڕێ بکە ⏳")

    # ئەگەر لینکەکە هی یوتوب بوو، سەرەتا بە API تاقی دەکاتەوە تا IP بلۆک نەبێت
    if "youtube.com" in url or "youtu.be" in url:
        try:
            api_url = "https://api.cobalt.tools/api/json"
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            payload = {"url": url}

            res = requests.post(api_url, json=payload, headers=headers, timeout=15)
            data = res.json()

            if "url" in data:
                file_url = data["url"]
                video_res = requests.get(file_url, stream=True)
                
                file_path = "yt_video.mp4"
                with open(file_path, "wb") as f:
                    for chunk in video_res.iter_content(chunk_size=1024*1024):
                        if chunk:
                            f.write(chunk)

                await update.message.reply_text("🎬 فایلی ڤیدیۆ (YouTube):")
                with open(file_path, "rb") as video:
                    await update.message.reply_video(video)

                if os.path.exists(file_path):
                    os.remove(file_path)
                await msg.delete()
                return
        except Exception:
            pass  # ئەگەر API نەبوو، دەچێتە سەر ڕێگەی دوم

    # بۆ Instagram, TikTok, Facebook و ڕێگەی دووەمی یوتوب
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'max_filesize': 50000000,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.exists(filename):
            with open(filename, 'rb') as video:
                await update.message.reply_video(video)
            os.remove(filename)
            await msg.delete()
        else:
            await msg.edit_text("فایلەکە نەدۆزرایەوە یان قەبارەکەی زۆر گەورەیە.")

    except Exception as e:
        await msg.edit_text(f"کێشەیەک لە یوتوب یان لینکەکەدا هەیە:\n{str(e)}")

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
