from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  
from aiogram import Dispatcher, Bot, executor, types
from bs4 import BeautifulSoup
import urllib.request as urllib
import wikipedia, re


# Токен бота NewsBot
API_TOKEN = "5970709075:AAF1Md9l0svi7wqxjlXt9gnQ0bnu0YlSEcE"

# инициализация бота
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")

def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всё после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x): 
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'

# Создание клавиатуры #
# Главная клавиатура
btn_Cpp = KeyboardButton('C++')
btn_Python = KeyboardButton('Python')
btn_Habr = KeyboardButton('Habr')
btn_other = KeyboardButton('Другое')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_Cpp, btn_Python, btn_Habr, btn_other)

# Возвратное меню
btn_info = KeyboardButton('Информация')
btn_main = KeyboardButton('Главное меню')

other_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_info, btn_main)

# Меню C++
btn_CppNews = KeyboardButton('Новости C++')
btn_CppProject = KeyboardButton('Проекты на C++')
btn_back = KeyboardButton('Назад')

second_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_CppNews, btn_CppProject, btn_back)

# Меню Python
btn_PythonNews = KeyboardButton('Новости Python')
btn_PythonProject = KeyboardButton('Проекты на Python')
btn_back = KeyboardButton('Назад')

third_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_PythonNews, btn_PythonProject, btn_back)

#  Приветствование после запуска
@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"👋 Привет, {message.from_user.first_name}! Выбери язык программирования, который тебя интересует, чтобы увидеть контент, который выкладывается на Habr.\nА также можешь воспользоваться Википедией, для этого нужно лишь ввести что интересует.", reply_markup = main_menu)

# Взаимодействие с меню
@dispatcher.message_handler()
async def messages(message: types.Message):
    url = ''
    if message.text == 'C++':
        await bot.send_message(message.from_user.id, 'Открываю C++...', reply_markup = second_menu)
    elif message.text == 'Новости C++':
        url = 'https://habr.com/ru/search/?q=C%2B%2B&target_type=posts&order=date'
    elif message.text == 'Проекты на C++':
        url = 'https://habr.com/ru/hub/cpp/'
    elif message.text == 'Назад':
        await bot.send_message(message.from_user.id, 'Возвращаюсь', reply_markup = main_menu)
    elif message.text == 'Python':
        await bot.send_message(message.from_user.id, 'Открываю Python', reply_markup = third_menu)
    elif message.text == 'Новости Python':
        url = 'https://habr.com/ru/search/?q=Python&target_type=posts&order=date'
    elif message.text == 'Проекты на Python':
        url = 'https://habr.com/ru/hub/python/'
    elif message.text == 'Назад':
        await bot.send_message(message.from_user.id, 'Возвращаюсь', reply_markup = main_menu)
    elif message.text == 'Habr':
        url = 'https://habr.com/ru/all/'
    elif message.text == 'Другое':
        await bot.send_message(message.from_user.id, 'Открываю...', reply_markup = other_menu)
    elif message.text == 'Информация':
        await bot.send_message(message.from_user.id, f'Бот создан для проекта.\nДля упрощения пользования сайтом Habr, чтобы быть всегда в курсе последних новостей.\nБот умеет выдавать последниее 3 актуальные новости, а также можно воспользоваться Википедией, для этого достаточно ввести слово или словосочетание ,или даже дату, и бот найдет значение того, что вы искали.\n\nСоздатели:\nКос Данил\nМедведев Виталий')
    elif message.text == 'Главное меню':
        await bot.send_message(message.from_user.id, 'Открываю меню...', reply_markup = main_menu)
    else:
        await bot.send_message(message.chat.id, getwiki(message.text))

    tag = 'a'
    class_tag = 'tm-article-snippet__title-link'
    url_site = 'habr.com'

    page = urllib.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    article_list = (soup.find_all(tag, attrs={'class': class_tag}))[:3]

    for i in article_list:
        article = f"{i.text.strip()}\n\n{url_site}{i['href']}"
        await bot.send_message(message.from_user.id, article)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)