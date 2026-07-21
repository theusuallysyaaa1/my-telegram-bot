import os
import requests
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8990062832:AAEGVGJum4r6erE25mqDFuSoah7zOdv1ShM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! سپاس بۆ هەڵبژاردن و بەکارهێنانی ئەم بۆتە ❤️\nتکایە لینکی (YouTube, Instagram, TikTok, Facebook) بنێرە تا بۆت دابەزێنم.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("دەستکرا بە پرۆسەی داگرتن... تکایە چاوەڕێ بکە ⏳")

    # هەوڵدان لە ڕێگەی APIی گشتییەوە بۆ تێپەڕاندنی بلۆکی IP
    try:
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        payload = {"url": url}

        res = requests.post(api_url, json=payload, headers=headers, timeout=20)
        data = res.json()

        if "url" in data:
            file_url = data["url"]
            video_res = requests.get(file_url, stream=True)
            
            file_path = "video.mp4"
            with open(file_path, "wb") as f:
                for chunk in video_res.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)

            await update.message.reply_text("🎬 فایلی ڤیدیۆ (Video):")
            with open(file_path, "rb") as video:
                await update.message.reply_video(video)

            if os.path.exists(file_path):
                os.remove(file_path)
            await msg.delete()
            return
    except Exception:
        pass  # ئەگەر APIەکە شکستی هێنا، ڕاستەوخۆ دەچێتە سەر ڕێگەی دووەم (yt-dlp)

    # ڕێگەی دووەم: بەکارهێنانی yt-dlp بە هاوشێوەکردنی ئایفۆن و ئەندرۆید
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_media.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android']
            }
        },
        'nocheckcertificate': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.exists(filename):
            await update.message.reply_text("🎬 فایلی ڤیدیۆ (Video):")
            with open(filename, 'rb') as media:
                await update.message.reply_video(media)
            os.remove(filename)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"کێشەیەک ڕوویدا لە کاتی داگرتندا:\nتکایە دڵنیابەرەوە لینکەکە ڕاستە یان دوابارە هەوڵ بدەرەوە.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    print("بۆتەکە چالاک کرا...")
    app.run_polling()

if __name__ == '__main__':
    main()
