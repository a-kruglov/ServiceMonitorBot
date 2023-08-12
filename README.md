# Service Monitor Bot

Service Monitor Bot is a Python-based bot that allows you to monitor, start, stop, and restart system services via Telegram. It leverages the `systemd` library to interact with system services and the `telebot` library to communicate with the Telegram API.

## Features

- Monitor specified system services
- Receive logs and notifications via Telegram
- Start, stop, and restart services directly from Telegram
- Check the status of services

## Requirements

- Python 3.x
- `telebot` library
- `systemd` library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/a-kruglov/ServiceMonitorBot
```

3. Install the required dependencies:
```bash
pip install telebot systemd
```

4. Edit the `config.py` file with your bot token, chat ID, and the services you want to monitor.

```bash
python main.py
```

## Usage

Once the bot is running, you can interact with it via Telegram to monitor and control the specified services.
![image](https://github.com/a-kruglov/ServiceMonitorBot/assets/66431153/d2174e51-dc23-4e60-9417-f288175ad155)


## Contributing

Feel free to fork the project, make changes, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or support, please contact the repository owner.
