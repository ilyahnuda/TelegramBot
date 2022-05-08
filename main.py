import json
import random
from PIL import Image
import telebot
from telebot import types
from nltk.chat.util import Chat, reflections
import wikipedia, re

pairs = [
    [
        r"Привет (.*)  как тебя зовут ?",
        ["Привет я бот, меня зовут Боб", "Привет, я Боб", "Меня зовут Боб"]
    ],
    [
        r"Как ты ?",
        ["У меня все хорошо", "Хорошо , а у тебя как ?"]
    ],
    [
        r"sorry (.*)",
        ["Все в порядке", "Не бери в голову", ]
    ],
    [
        r"Я в порядке",
        ["Рад слышать это, могу ли я чем-то помочь тебе?", ]
    ],
    [
        r"У меня (.*) хорошо",
        ["Рад слышать это, могу ли я чем-то помочь тебе?", ]
    ],
    [
        r"(.*) ты можешь (.*)*",
        ["Мы можем просто с вам пообщаться либо вы можете  написать /start и я покажу некоторые свои функции",
         "Пропиши /start"]
    ],
    [
        r"(.*) космос[а-я]+ (.*)*",
        ["Космос это поразительная вещь, трудно даже представить насколько он большой", "Ко́смос (др.-греч. κόσμος — "
                                                                                        "«упорядоченность», "
                                                                                        "«порядок») — относительно "
                                                                                        "пустые участки Вселенной, "
                                                                                        "которые лежат вне границ "
                                                                                        "атмосфер небесных тел. Космос "
                                                                                        "не является абсолютно пустым "
                                                                                        "пространством: в нём есть, "
                                                                                        "хотя и с очень низкой "
                                                                                        "плотностью, межзвёздное "
                                                                                        "вещество (преимущественно "
                                                                                        "молекулы водорода), "
                                                                                        "кислород в малых количествах "
                                                                                        "(остаток после взрыва "
                                                                                        "звезды), космические лучи и "
                                                                                        "электромагнитное излучение, "
                                                                                        "а также гипотетическая тёмная "
                                                                                        "материя."]
    ],
    [
        r"(.*) о планет[а-я]+ (.*)?",
        ["Это большие шары в невесомости",
         " небесное тело, вращающееся по орбите вокруг звезды или её остатков, достаточно массивное, чтобы стать округлым под действием собственной гравитации, но недостаточно массивное для начала термоядерной реакции",
         "Их можно поделить на твердые и газовые, последних кстати больше всего"]

    ],
    [
        r"(.*) поподробней об звезд[а-я]+ (.*)*",
        ["Самая близкая звезда к нас это Солнце",
         "Вообще там происходит термоядерны реакции, а сами они состоят из водорода и гелия в основном"]
    ],
    [
        r"(.*) Альфа-Центаврна (.*)*",
        ["Да это звезда, ближайшая к нам звезда не включая Солнце",
         "Вообще там происходит термоядерны реакции, а сами они состоят из водорода и гелия в основном"]
    ],
    [
        r"(.*) звезд[а-я]+ (.*)*",
        ["Это источники огромной энергии и тепла",
         "Это как планеты только горячие"]
    ],
    [
        r"(.*) о вселенн[а-я]+ (.*)*",
        ["Это выше моего понимания",
         "Это все сущее",
         "Это место где все расширяется и вроде бы с ним связан сериал Большой взрыв"]
    ],
    [
        r"(.*)  Земле[а-я] (.*)*",
        ["Мы тут живем",
         "Земля́ — третья по удалённости от Солнца планета Солнечной системы. Самая плотная, пятая по диаметру и массе среди всех планет и крупнейшая среди планет земной группы, в которую входят также Меркурий, Венера и Марс. Единственное известное человеку в настоящее время тело во Вселенной, населённое живыми организмами."]
    ],
    [
        r"(.*) (одни|одиноки|другие формы жизни|существуют ли инопланетяне) (.*)*",
        ["Хмм...... сложно",
         "Трудно утверждать или опровергать эту гипотезу, учитывая что большинство данных о других галктиках приходят до нас с опозданием на несколько миллинок лет",
         "Думаю да"]
    ],
    [
        r"(.*)  (С|с)олнечная систем[а-я] (.*)*",
        [
            "Это  планетная система, включающая в себя центральную звезду Солнце и все естественные космические объекты, вращающиеся вокруг Солнца. Она сформировалась путём гравитационного сжатия газопылевого облака примерно 4,57 млрд лет назад",
            " Солнечная система состоит из двух областей, также в ней находятся 8 планет включая нашу"]
    ],
    [
        r"(.*)  нравится космос (.*)*",
        ["Да определенно а вам", "Конечно, это как быть первооткрывателм"]
    ],
    [
        r"Да мне нравится",
        ["Ух ты я рад у нас схожие интересы", "А вам что именно нравится?"]
    ],
    [
        r"(.*)  (нравится|предпочитаю) (.*)*",
        ["Интересно, а мне нравятся изучать звезды можешь написать /stars и прочитаешь про мои любимые звезды"]
    ],
    [
        r"(.*)  Стивен Хокинг (.*)*",
        ["Один  из самый узнаваемых астрофизиков, а его вклад в изучение черных дыр сложно переоценить", "Астрофизик"]
    ],
    [
        r"(.*)  факт[а-я]  Стивене Хокинге (.*)*",
        ["В его честь названо однин явление, которое он же и открыл.Излучение Хокинга"]
    ],
    [
        r"(.*)  излучение хокинга (.*)*",
        [
            "Черные дыры с течение времени испоряются. Это связано с тем что в черных дырах создаются атомы и сразу же расщепляются и одна такая часть улетучивается"]
    ],
    [
        r"(.*)  расскажи  (.*)*",
        [
            "Нажми /start и выбери что хочешь чтоб я рассказал"]
    ],
    [
        r"(.*)",
        [
            "Ой, я не знаю как на это ответить",
            "Спроси лушче что-нибудь другие",
            "Кожаный, иди лучше ляж"
        ]
    ]
]
TOKEN = "5304895210:AAGhJSI6JLeaIToTdTUlt0sLCk5sIHuNT_8"
bot = telebot.TeleBot(TOKEN)
chat = Chat(pairs, reflections)


@bot.message_handler(commands=['start'])
def start_function(message):
    bot.send_message(message.chat.id, "Функции:\n"
                                      "/stars -- просмотр звезд\n"
                                      "/planets --  просмотр планет\n"
                                      "/galaxies -- информация о галактиках\n"
                                      "/facts -- факт о космосе")


@bot.message_handler(commands=['stars'])
def db_stars(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Альферац', callback_data='Alf'))
    markup.add(types.InlineKeyboardButton(text="Стеферсон", callback_data='Stephenson'))
    markup.add(types.InlineKeyboardButton(text="RW Цефея", callback_data='RW'))
    markup.add(types.InlineKeyboardButton(text="Звезда́ Ван Маа́нена", callback_data='Van'))
    markup.add(types.InlineKeyboardButton(text="Солнце", callback_data='Sun'))

    bot.send_message(message.from_user.id, text='Выберите звезду', reply_markup=markup)


@bot.message_handler(commands=['planets'])
def db_stars(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Марс', callback_data='planet_Mars'))
    markup.add(types.InlineKeyboardButton(text="Сатурн", callback_data='planet_Saturn'))
    markup.add(types.InlineKeyboardButton(text="Kepler-1649 c", callback_data='planet_Kepler'))
    markup.add(types.InlineKeyboardButton(text="Проксима Центавра b", callback_data='planet_Proxima'))
    markup.add(types.InlineKeyboardButton(text="Росс 128 b", callback_data='planet_Ross'))

    bot.send_message(message.from_user.id, text='Выберите планету', reply_markup=markup)


@bot.message_handler(commands=['galaxies'])
def db_stars(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Млечный путь', callback_data='galaxy_MW'))
    markup.add(types.InlineKeyboardButton(text="Туманность Андромеды", callback_data='galaxy_M31'))
    markup.add(types.InlineKeyboardButton(text="Галактика Водоворот(M 51)", callback_data='galaxy_M51'))

    bot.send_message(message.from_user.id, text='Выберите галактику', reply_markup=markup)


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext = ny.content[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные
                # при разделении строк точки на место
                if len((x.strip())) > 3:
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


@bot.message_handler(commands=['definition'])
def db_def(message):
    bot.send_message(message.chat.id, getwiki(message.text))


@bot.message_handler(commands=['facts'])
def start_conversation(message):
    res = str(get_facts())
    bot.send_message(message.chat.id, res)


@bot.message_handler(content_types=["text"])
def start_conversation(message):
    answer = chat.respond(message.text)
    bot.send_message(message.chat.id, answer)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    dir1 = "stars"
    str1 = str(call.data)
    if str1.startswith("planet_"):
        str1 = str(call.data)[len("planet_"):]
        dir1 = 'planets'
    elif str1.startswith("galaxy_"):
        str1 = str(call.data)[len("galaxy_"):]
        dir1 = 'galaxies'
    img = load_img(dir1, str1)
    bot.send_photo(call.message.chat.id, img)
    if dir1 == 'planets':
        object1 = get_planets(str1)
    elif dir1 == 'galaxies':
        object1 = get_galaxies(str1)
    else:
        object1 = get_stars(str1)
    bot.send_message(call.message.chat.id, from_json_to_str(object1))


def load_img(dir1, name):
    path = f"images/{dir1}/{name}.jpg"
    img = Image.open(path)
    return img


def loads_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        templates = json.load(f)
    return templates


def get_facts(facts={}):
    if len(facts) == 0:
        facts = loads_json('DB/facts.json')
    fact = facts[str(random.randint(1, 10))]
    print(facts)
    return "Интересеный факт:\n" + (from_json_to_str(fact))


def get_stars(star, stars={}):
    if len(stars) == 0:
        stars = loads_json('DB/stars.json')
    fact = dict(stars[star])
    return fact


def get_planets(plan, planets={}):
    if len(planets) == 0:
        planets = loads_json('DB/planets.json')
    fact = dict(planets[plan])
    return fact


def get_galaxies(galaxy, galaxies={}):
    if len(galaxies) == 0:
        galaxies = loads_json('DB/galaxies.json')
    fact = dict(galaxies[galaxy])
    return fact


def from_json_to_str(dict1: dict):
    strin = dict1['body'] + "\n"
    if 'temperature' in dict1:
        strin = strin + "Температура:" + dict1['temperature'] + "\n"
    if 'Type' in dict1:
        strin = strin + "Тип планеты:" + dict1['Type'] + "\n"
    if 'Mass' in dict1:
        strin = strin + "Масса:" + dict1['Mass'] + "\n"
    if 'luminosity' in dict1:
        strin = strin + "Светимость:" + dict1['luminosity'] + "\n"
    return strin


bot.polling(none_stop=True, interval=0)
