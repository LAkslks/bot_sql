import telebot
import psycopg2
from telebot import types


# подключение к PostgreSQL
db_params = {
        'database':'name',
        'user' : 'user',
        'password' : 'password',
        'port' : 'port'
}


# Функция для добавления данных в базу
def add_data_to_db(id, data):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO tasks (id, task) VALUES (%s, %s)', (id, data))
            conn.commit()

# Функция для извлечения данных из базы
def get_tasks_from_db(id):
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT task FROM tasks WHERE id = %s', (id,))
            tasks = cursor.fetchall()
            return tasks


bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands = ['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
    keyboard.add(types.KeyboardButton('/add'))
    keyboard.add(types.KeyboardButton('/tsk'))
    bot.send_message(message.chat.id, 'Здравствуйте, этот бот создает задачи и запрашивает их add- добавляет, tsk- извликает', reply_markup=keyboard)
    

@bot.message_handler(func=lambda message: message.text == '/add')
def handle_add(message):
    read = bot.send_message(message.chat.id, 'Введите задачу:')
    bot.register_next_step_handler(read, none_add_commands, message.from_user.id)


def none_add_commands(message, id):
    add_data_to_db(id, message.from_user.id)
    bot.send_message(message.chat.id, 'Данные добавлены.')
    
    
    
# Обработчик команды /tsk
@bot.message_handler(func=lambda message: message.text == '/tsk')
def handle_tsk(message):
    tasks = get_tasks_from_db(message.from_user.id)
    response = '\n'.join(task[0] for task in tasks)
    bot.send_message(message.chat.id, response)
    
bot.polling(none_stop=True)
