import subprocess
import threading
import time
import telebot
from config import bot_token, chat_id, services_to_monitor

from telebot import types
from systemd import journal


bot = telebot.TeleBot(bot_token)


def send_buffer(service_name, buffer):
    if buffer:
        header = f"📢 Logs from {service_name} 📢\n"
        message = header + ''.join(buffer)
        markup = types.InlineKeyboardMarkup()
        restart_button = types.InlineKeyboardButton(text="Restart service", callback_data=f'restart|{service_name}')
        start_button = types.InlineKeyboardButton(text="Start service", callback_data=f'start|{service_name}')
        stop_button = types.InlineKeyboardButton(text="Stop service", callback_data=f'stop|{service_name}')
        status_button = types.InlineKeyboardButton(text="Service status", callback_data=f'status|{service_name}')
        markup.add(restart_button, start_button, stop_button, status_button)
        bot.send_message(chat_id, message[:4000], reply_markup=markup)


def start_service(service_name):
    subprocess.run(['sudo', 'systemctl', 'start', service_name])
    bot.send_message(chat_id, f"Service {service_name} has been started ▶️")


def stop_service(service_name):
    subprocess.run(['sudo', 'systemctl', 'stop', service_name])
    bot.send_message(chat_id, f"Service {service_name} has been stopped ⏹️")


def check_status(service_name):
    result = subprocess.run(['sudo', 'systemctl', 'is-active', service_name], stdout=subprocess.PIPE)
    status = result.stdout.decode().strip()
    status_emoji = '✅' if status == 'active' else '❌'

    message = f"Status of {service_name}: {status_emoji} {status.capitalize()}"
    bot.send_message(chat_id, message)


def restart_service(service_name):
    subprocess.run(['sudo', 'systemctl', 'restart', service_name])
    bot.send_message(chat_id, f"Service {service_name} has been restarted 🔄")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    action, service_name = call.data.split('|', 1)
    if action == 'restart':
        restart_service(service_name)
    elif action == 'start':
        start_service(service_name)
    elif action == 'stop':
        stop_service(service_name)
    elif action == 'status':
        check_status(service_name)
    bot.answer_callback_query(call.id, f"{action.capitalize()}ing {service_name}...")


def monitor_logfiles():
    j = journal.Reader()
    j.this_boot()
    j.log_level(journal.LOG_INFO)
    last_timestamps = {service: None for service in services_to_monitor}

    while True:
        for service in services_to_monitor:
            j.flush_matches()
            j.add_match(_SYSTEMD_UNIT=service)
            j.seek_head()
            buffer = []

            for entry in j:
                if last_timestamps[service] is not None and entry['__REALTIME_TIMESTAMP'] <= last_timestamps[service]:
                    continue

                buffer.append(entry['MESSAGE'] + '\n')
                last_timestamps[service] = entry['__REALTIME_TIMESTAMP']

            if buffer:
                send_buffer(service, buffer)

        time.sleep(10)


threading.Thread(target=monitor_logfiles).start()
bot.polling(none_stop=True)
