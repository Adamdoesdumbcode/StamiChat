import json
import time

# File to keep track of banned users
BAN_FILE = 'banned_users.json'

def load_banned_users():
    try:
        with open(BAN_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_banned_users(banned_users):
    with open(BAN_FILE, 'w') as file:
        json.dump(banned_users, file)

def ban_user(ip, duration):
    banned_users = load_banned_users()
    banned_users[ip] = {'duration': duration, 'timestamp': time.time()}
    save_banned_users(banned_users)
    print(f'User with IP {ip} has been banned for {duration}.')

def unban_user(ip):
    banned_users = load_banned_users()
    if ip in banned_users:
        del banned_users[ip]
        save_banned_users(banned_users)
        print(f'User with IP {ip} has been unbanned.')
    else:
        print(f'No ban found for IP {ip}.')

def list_banned_users():
    banned_users = load_banned_users()
    if banned_users:
        print('Banned Users:')
        for ip, info in banned_users.items():
            print(f'IP: {ip}, Duration: {info["duration"]} seconds, Banned At: {info["timestamp"]}')
    else:
        print('No banned users.')

def main():
    while True:
        print("\nAdmin Terminal")
        print("1. Ban User")
        print("2. Unban User")
        print("3. List Banned Users")
        print("4. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            ip = input("Enter IP address to ban: ")
            duration = int(input("Enter ban duration in seconds: "))
            ban_user(ip, duration)
        elif choice == '2':
            ip = input("Enter IP address to unban: ")
            unban_user(ip)
        elif choice == '3':
            list_banned_users()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
