from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from pdf_generator import generate_pdf
import os

# Holatlar
(ASK_FULLNAME, ASK_PHOTO_CHOICE, ASK_PHOTO, ASK_JOB, ASK_EDUCATION,
 ASK_SKILLS, ASK_EXPERIENCE, ASK_CONTACT, ASK_LINKS, ASK_DESIGN) = range(10)

user_data_dict = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! 👋\nMen Resume yaratuvchi botman.\nBoshlaymiz!\n\nIsm va familiyangizni to‘liq kiriting:")
    return ASK_FULLNAME

async def get_fullname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id] = {"fullname": update.message.text}
    reply_keyboard = [["Rasmli", "Rasmsiz"]]
    await update.message.reply_text(
        "Resume rasmli bo‘lsinmi yoki rasmsiz?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return ASK_PHOTO_CHOICE

async def get_photo_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    choice = update.message.text.lower()

    if "rasmli" in choice:
        await update.message.reply_text("Iltimos, rasm yuboring 📸")
        return ASK_PHOTO
    else:
        user_data_dict[user_id]["photo"] = None
        await update.message.reply_text("Kasbingiz yoki lavozimingizni kiriting:")
        return ASK_JOB

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()

    os.makedirs("photos", exist_ok=True)
    photo_path = f"photos/{user_id}.jpg"
    await photo_file.download_to_drive(photo_path)

    user_data_dict[user_id]["photo"] = photo_path
    await update.message.reply_text("✅ Rasm saqlandi!\nEndi kasbingiz yoki lavozimingizni kiriting:")
    return ASK_JOB

async def get_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_dict[update.message.from_user.id]["job"] = update.message.text
    await update.message.reply_text("Ta’lim ma’lumotingizni yozing:")
    return ASK_EDUCATION

async def get_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_dict[update.message.from_user.id]["education"] = update.message.text
    await update.message.reply_text("Ko‘nikmalaringizni yozing:")
    return ASK_SKILLS

async def get_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_dict[update.message.from_user.id]["skills"] = update.message.text
    await update.message.reply_text("Tajriba (ish joylari, loyihalar, va hokazo):")
    return ASK_EXPERIENCE

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_dict[update.message.from_user.id]["experience"] = update.message.text
    await update.message.reply_text("Aloqa ma’lumotlaringizni kiriting (telefon, email, telegram):")
    return ASK_CONTACT

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data_dict[update.message.from_user.id]["contact"] = update.message.text
    await update.message.reply_text("Qo‘shimcha linklar (GitHub, LinkedIn, portfoliolar):")
    return ASK_LINKS

async def get_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data_dict[user_id]["links"] = update.message.text

    reply_keyboard = [["Zamonaviy", "Klassik", "Ijodiy"]]
    await update.message.reply_text(
        "Endi dizayn turini tanlang 🎨:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return ASK_DESIGN

async def get_design(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    design = update.message.text
    user_data = user_data_dict[user_id]

    # PDF yaratish
    os.makedirs("pdfs", exist_ok=True)
    pdf_path = f"pdfs/{user_id}_resume.pdf"
    generate_pdf(user_data, pdf_path, design)

    await update.message.reply_text("✅ Sizning resume tayyor! Quyida yuklab olishingiz mumkin:")
    await update.message.reply_document(open(pdf_path, "rb"))
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi ❌")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("8449999926:AAH9rbkl6SLaGKFCpo4ue5_x3Sm0IJufw2U").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fullname)],
            ASK_PHOTO_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_photo_choice)],
            ASK_PHOTO: [MessageHandler(filters.PHOTO, save_photo)],
            ASK_JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_job)],
            ASK_EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_education)],
            ASK_SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_skills)],
            ASK_EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            ASK_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
            ASK_LINKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_links)],
            ASK_DESIGN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_design)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Bot ishlayapti...")
    app.run_polling()

if __name__ == "__main__":
    main()
