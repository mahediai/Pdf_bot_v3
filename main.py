import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import PyPDF2
import io

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ভাই PDF ফাইল পাঠান। আমি Text বের করে দিবো ✅")

async def pdf_to_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document and update.message.document.mime_type == 'application/pdf':
        await update.message.reply_text("PDF পড়তেছি... ২ সেকেন্ড ⏳")
        
        pdf_file = await update.message.document.get_file()
        pdf_bytes = await pdf_file.download_as_bytearray()
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        if text:
            for i in range(0, len(text), 4000):
                await update.message.reply_text(text[i:i+4000])
        else:
            await update.message.reply_text("ভাই এই PDF থেকে Text পাইলাম না ❌")
    else:
        await update.message.reply_text("শুধু PDF ফাইল পাঠান ভাই")

def main():
    TOKEN = "YOUR_BOT_TOKEN_HERE" 
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, pdf_to_text))
    app.run_polling()

if __name__ == '__main__':
    main()
