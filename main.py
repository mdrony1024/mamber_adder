import time
import random
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, PeerFloodError

# আপনার তথ্য দিন
api_id = 21678674 
api_hash = 'c735dd88db95b39fefdb0e1798da1023'
target_group = 'https://t.me/theronystudio' # আপনার নতুন গ্রুপের ইউজারনেম (উদা: @my_group)
source_group = 'https://t.me/PromoteOstad' # যেখান থেকে মেম্বার নিবেন

client = TelegramClient('my_session', api_id, api_hash)

async def main():
    print(f"{source_group} থেকে মেম্বার সংগ্রহ করা হচ্ছে...")
    try:
        # সোর্স গ্রুপ থেকে ২০০ জন মেম্বার লিস্ট নেওয়া
        participants = await client.get_participants(source_group, limit=200)
        print(f"মোট {len(participants)} জন মেম্বার পাওয়া গেছে।")

        added_count = 0
        for user in participants:
            # আইডি সেফ রাখতে একবারে ৩০-৫০ জনের বেশি অ্যাড করবেন না
            if added_count >= 50: 
                print("আজকের মতো ৫০ জন অ্যাড শেষ। আইডি সুরক্ষার জন্য বট বন্ধ হচ্ছে।")
                break
                
            if user.bot or user.self:
                continue

            try:
                # মেম্বারকে আপনার গ্রুপে অ্যাড করা
                await client(InviteToChannelRequest(target_group, [user]))
                added_count += 1
                print(f"{added_count}. সফলভাবে অ্যাড হয়েছে: {user.first_name}")
                
                # প্রতিটি অ্যাডের মাঝে ৩০ থেকে ৬০ সেকেন্ড র‍্যান্ডম বিরতি
                sleep_time = random.randint(30, 60)
                print(f"নিরাপত্তার জন্য {sleep_time} সেকেন্ড অপেক্ষা করছি...")
                time.sleep(sleep_time)

            except FloodWaitError as e:
                print(f"টেলিগ্রাম থেকে বাধা! {e.seconds} সেকেন্ড অপেক্ষা করতে হবে।")
                time.sleep(e.seconds)
            except UserPrivacyRestrictedError:
                print(f"ইউজার {user.id}-এর প্রাইভেসি সেটিং এর কারণে অ্যাড করা যায়নি।")
            except PeerFloodError:
                print("অ্যাকাউন্ট স্প্যাম হিসেবে শনাক্ত হয়েছে! আজ আর চেষ্টা করবেন না।")
                return
            except Exception as e:
                print(f"ভুল: {e}")
                continue

    except Exception as e:
        print(f"গ্রুপ থেকে লিস্ট নিতে সমস্যা: {e}")

with client:
    client.loop.run_until_complete(main())
