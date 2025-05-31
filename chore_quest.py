import os
import json

SAVE_FILE = "chore_quest_save.json"

tasks = {
    "Gather Lost Artifacts": 20,
    "Defeat the Dust Demons": 20,
    "Sort the Scrolls of Knowledge": 20,
    "Conquer the Kitchen Chaos": 20,
}

buffs = {
    "Orderly Mind": {"active": False, "duration": 0, "bonus_xp": 5}
}

def get_rank(total_xp):
    if total_xp >= 1100:
        return "Grand Monarch of Cleanliness"
    elif total_xp >= 800:
        return "Master of the Realm"
    elif total_xp >= 500:
        return "Adept Cleanser"
    elif total_xp >= 200:
        return "Apprentice Order Keeper"
    else:
        return "Novice Tidy Warrior"

def load_save():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    else:
        return {"total_xp": 0, "buffs": {}}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def apply_buffs(xp, data):
    bonus = 0
    if data["buffs"].get("Orderly Mind", False):
        bonus += buffs["Orderly Mind"]["bonus_xp"]
    return xp + bonus

def update_buffs(data):
    to_remove = []
    for buff in list(data["buffs"]):
        data["buffs"][buff] -= 1
        if data["buffs"][buff] <= 0:
            to_remove.append(buff)
    for buff in to_remove:
        print(f"Buff {buff} has expired.")
        del data["buffs"][buff]

def main():
    print("=== Welcome to The Realm of the Tidy Keep ===\n")
    
    data = load_save()
    update_buffs(data)

    daily_xp = 0
    print(f"Current Total XP: {data['total_xp']}\nYour Rank: {get_rank(data['total_xp'])}\n")

    for task, xp in tasks.items():
        done = input(f"Did you complete '{task}'? (y/n): ").strip().lower()
        if done == "y":
            earned = apply_buffs(xp, data)
            print(f"Task completed! You earned {earned} XP.\n")
            daily_xp += earned
        else:
            print(f"Task skipped. No XP earned.\n")

    time = input("Did you finish all tasks under 60 minutes? (y/n): ").strip().lower()
    if time == "y":
        print("Swift Hands buff activated! +10 XP bonus.")
        daily_xp += 10

    new_total = data["total_xp"] + daily_xp
    if data["total_xp"] < 200 <= new_total:
        print("Congratulations! You unlocked 'Orderly Mind' buff for 3 days (+5 XP per task).")
        data["buffs"]["Orderly Mind"] = 3

    data["total_xp"] = new_total
    print(f"\nToday's Total XP earned: {daily_xp}")
    print(f"Overall Total XP: {data['total_xp']}")
    print(f"Your Rank is now: {get_rank(data['total_xp'])}")

    save_data(data)
    print("\nProgress saved. Keep questing!")

if __name__ == "__main__":
    