import time
import random
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, PeerFloodError

# আপনার তথ্য ঠিকঠাক দিন
api_id = 21678674 
api_hash = 'c735dd88db95b39fefdb0e1798da1023'
target_channel = '@theronystudio' # আপনার চ্যানেল ইউজারনেম
target_group = '@theronytop'     # আপনার গ্রুপ ইউজারনেম
source_group = 'https://t.me/PromoteOstad' # সোর্স গ্রুপ

client = TelegramClient('my_session', api_id, api_hash)

async def main():
    print(f"{source_group} থেকে মেম্বার সংগ্রহ করা হচ্ছে...")
    try:
        # মেম্বার লিস্ট সংগ্রহ
        participants = await client.get_participants(source_group, limit=200)
        print(f"মোট {len(participants)} জন মেম্বার পাওয়া গেছে।")

        added_count = 0
        for user in participants:
            if added_count >= 60: 
                print("আজকের মতো লিমিট (৬০ জন) শেষ!")
                break
                
            # এখানে ভুলটি ঠিক করা হয়েছে (is_self)
            if user.bot or user.is_self: 
                continue

            print(f"চেষ্টা করা হচ্ছে: {user.first_name}")

            # ১. চ্যানেলে অ্যাড করার চেষ্টা
            try:
                await client(InviteToChannelRequest(target_channel, [user]))
                print(f"চ্যানেলে অ্যাড হয়েছে: {user.first_name}")
            except Exception as e:
                # চ্যানেলে ২০০ জন পূর্ণ হলে এখানে এরর দেখাবে, এটা স্বাভাবিক
                print(f"চ্যানেলে হলো না: {e}")

            # ২. গ্রুপে অ্যাড করার চেষ্টা
            try:
                await client(InviteToChannelRequest(target_group, [user]))
                added_count += 1
                print(f"গ্রুপে অ্যাড হয়েছে: {user.first_name}")
            except Exception as e:
                print(f"গ্রুপে হলো না: {e}")

            # আইডি সেফ রাখতে ৩০-৬০ সেকেন্ড বিরতি
            wait_time = random.randint(30, 60)
            print(f"অপেক্ষা করছি {wait_time} সেকেন্ড...\n")
            time.sleep(wait_time)

    except FloodWaitError as e:
        print(f"টেলিগ্রাম বাধা দিয়েছে! {e.seconds} সেকেন্ড অপেক্ষা করতে হবে।")
        time.sleep(e.seconds)
    except Exception as e:
        print(f"ভুল হয়েছে: {e}")

with client:
    client.loop.run_until_complete(main())
