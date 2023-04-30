import os
import telebot

BOT_TOKEN = "5916910739:AAHQC0W_LIZow6xO_OIk-BDtAZvWQsS6fU4"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Hi! Please enter your email address:")

@bot.message_handler(func=lambda message: True)
def email_message(message):
    email = message.text
    bot.reply_to(message, "Thanks! Please enter your email password:")
    bot.register_next_step_handler(message, password_message, email)

def password_message(message, email):
    password = message.text
    bot.reply_to(message, "Thanks! Please upload your folder:")
    bot.register_next_step_handler(message, folder_message, email, password)

# get the path to the desktop folder
desktop_path = os.path.join(os.path.join(os.environ['HOME']), 'Desktop')


def folder_message(message, email, password):
    folder_id = message.document.file_id
    folder_path = bot.download_file(folder_id)

    # create the path to the folder on the desktop
    folder_name = message.document.file_name
    folder_save_path = os.path.join(desktop_path, 'my_folders', folder_name)

    # save the folder to disk
    with open(folder_save_path, 'wb') as f:
        f.write(folder_path)

    bot.reply_to(message, "Thanks! Your email is {}, password is {} and folder path is {}".format(email, password, folder_save_path))
bot.polling()
