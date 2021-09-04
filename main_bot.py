def launch_bot():
    import telebot
    from telebot import types
    import urllib
    import scan_worker
    import time
    import cv2
    import scanning
    import jpg_to_pdf
    import os

    ###########################################################
    k = 1
    list_of_photos = []
    greet_keyboard = types.ReplyKeyboardMarkup()
    btn_act1 = types.KeyboardButton('JPG to PDF')
    btn_act2 = types.KeyboardButton('Нормализовать Картинку')
    btn_act3 = types.KeyboardButton('Отнормализовать документ и отправить в PDF')
    greet_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(btn_act1).add(btn_act2).add(btn_act3)

    ###########################################################

    bot = telebot.TeleBot('1715724358:AAE4L9brmOJ9izvZ2ajaFq_u11URAt3kRzo')

    @bot.message_handler(commands=['start'])
    def get_text_messages(message):
        if message.text == "/start":
            print("User launch the bot.")
            bot.send_message(message.from_user.id, "Привет! Выбери, что ты хочешь от меня.",
                             reply_markup=greet_keyboard)
            bot.register_next_step_handler(message, call_photo)
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши /start")
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

    def call_photo(message):
        nonlocal list_of_photos
        if message.text == 'Нормализовать Картинку':
            print("User chose \"Нормализовать картинку\".")
            bot.send_message(message.from_user.id, "Отправь фото с документом. Положи его на стол или"
                                                   " на другую поверхность, чтобы документ выделялся цветом.\n"
                                                   "Тогда я с большей вероятностью выдам тебе, что ты хочешь)")
            bot.register_next_step_handler(message, get_scanned)
        elif message.text == 'JPG to PDF':
            print("User chose \"JPG to PDF\".")
            bot.send_message(message.from_user.id, "Отправляй фотки. Я отправлю тебе PDF.\n "
                                                   "Это займет примерно 20 секунд. ")

            list_of_photos = []

            while list_of_photos == []:
                continue

            time.sleep(15)

            print("saved paths: ", list_of_photos)
            print("launch JPG_to_PDF... ")

            jpg_to_pdf.several_photos(list_of_photos)

            bot.send_document(message.from_user.id, data=open('PDF/my.pdf', 'rb'))

            print("Send pdf to user.")

            for path in list_of_photos:
                os.remove(path)
            list_of_photos = []

            os.remove("PDF/my.pdf")

            print("PDF file and photos were deleted.")

            bot.send_message(message.from_user.id, "Если хочешь еще, то начинай заново со /start.")

        elif message.text == 'Отнормализовать документ и отправить в PDF':
            print("User chose \"Отнормализовать документ и отправить в PDF\".")
            bot.send_message(message.from_user.id, "Отправляй фотки. Я их нормализую и отправлю тебе PDF.\n "
                                                   "Это займет примерно минуту.")

            list_of_photos = []

            while list_of_photos == []:
                continue

            time.sleep(15)
            paths = []
            photos_for_delete = []
            temp = 0
            for src in list_of_photos:
                saved, temp_list_paths = scanning.scanner(src, temp)
                paths.append(saved)
                photos_for_delete += temp_list_paths
                temp += 1
                print(src + " has been scanned.")
            print("Scanned paths: ", paths)
            print("launch JPG to PDF...")

            jpg_to_pdf.several_photos(paths)

            bot.send_document(message.from_user.id, data=open('PDF/my.pdf', 'rb'))
            print("Send pdf to user.")

            # print(photos_for_delete)

            for path in list_of_photos:
                os.remove(path)
            list_of_photos = []
            os.remove("PDF/my.pdf")
            for path in photos_for_delete:
                os.remove(path)
            print("Sent photos, scanned photos, pdf file were deleted.")

            bot.send_message(message.from_user.id, "Если хочешь еще, то начинай заново со /start.")

    def get_scanned(message):
        bot.send_message(message.from_user.id, "Понял, жди.")
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = file_info.file_path
        with open(src, "wb") as new_file:
            new_file.write(downloaded_file)
        print("Photo has been saved to ", src)
        time.sleep(5)
        bot.send_message(message.from_user.id, "Сохранил у себя. Сейчас обработаю...")
        saved, paths = scanning.scanner(src, 1)

        for path in paths:
            bot.send_photo(message.from_user.id, photo=open(path, 'rb'))

        print("Deleting these: ", src + " " + " ".join(paths))

        os.remove(src)
        for path in paths:
            os.remove(path)

        print("Photos were deleted.")

        bot.send_message(message.from_user.id, "Если хочешь еще, то начинай заново со /start.")

    @bot.message_handler(content_types=['photo'])
    def handle_docs_photo(message):
        nonlocal k
        nonlocal list_of_photos
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        src = "photos/saved_to_pdf_" + str(k) + ".jpg"
        k += 1

        list_of_photos.append(src)

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        print("Temporary photo \"" + src + "\" has been saved.")

        # bot.reply_to(message, "Пожалуй, я сохраню это")

    bot.polling(none_stop=True, interval=0)
