import time
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest

api_id = 21678674 
api_hash = 'c735dd88db95b39fefdb0e1798da1023'
target_channel = '@theronystudio'
source_group = '@FF_Community_BD' # উদা: '@test_group'

client = TelegramClient('my_session', api_id, api_hash)

async def main():
    try:
        print(f"{source_group} থেকে মেম্বার সংগ্রহ করা হচ্ছে...")
        participants = await client.get_participants(source_group, limit=100)
        
        if not participants:
            print("কোনো মেম্বার পাওয়া যায়নি। গ্রুপটি হয়তো প্রাইভেট বা লিস্ট হাইড করা।")
            return

        for user in participants:
            try:
                if user.bot: continue
                await client(InviteToChannelRequest(target_channel, [user]))
                print(f"অ্যাড হয়েছে: {user.first_name}")
                time.sleep(20)
            except Exception as e:
                print(f"অ্যাড করা যায়নি: {e}")
                continue
    except Exception as e:
        print(f"ভুল হয়েছে: {e}")

with client:
    client.loop.run_until_complete(main())

from telethon.tl.functions.channels import GetFullChannelRequest

# ... আগের কোড ...

async def main():
    # চ্যানেলে বর্তমানে কতজন আছে তা চেক করা
    full_channel = await client(GetFullChannelRequest(target_channel))
    current_count = full_channel.full_chat.participants_count
    
    print(f"বর্তমানে চ্যানেলে মেম্বার আছে: {current_count}")

    if current_count >= 200:
        print("দুঃখিত! চ্যানেলে ২০০ জন পূর্ণ হয়ে গেছে। আর মেম্বার অ্যাড করা যাবে না।")
        return # এখানেই কোড থেমে যাবে

    # ... এরপর মেম্বার অ্যাডিং শুরু হবে ...
