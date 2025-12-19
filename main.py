import time
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import Channel, Chat
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, PeerFloodError

# আপনার তথ্য দিন
api_id = 21678674 
api_hash = 'c735dd88db95b39fefdb0e1798da1023'
target_channel_username = '@theronystudio' # আপনার নিজের চ্যানেল যেখানে মেম্বার নিবেন

client = TelegramClient('my_session', api_id, api_hash)

async def main():
    # আপনার টার্গেট চ্যানেলকে চিনে নেওয়া
    target_entity = await client.get_input_entity(target_channel_username)
    
    total_added = 0
    LIMIT = 200 # টেলিগ্রামের সর্বোচ্চ ডেইলি লিমিট

    print("আপনার সব গ্রুপ থেকে মেম্বার খোঁজা হচ্ছে...")
    
    # সব ডায়ালগ (চ্যাট/গ্রুপ/চ্যানেল) চেক করা
    async for dialog in client.iter_dialogs():
        if total_added >= LIMIT:
            break
            
        # শুধুমাত্র গ্রুপ বা সুপারগ্রুপ থেকে মেম্বার নেওয়া সম্ভব (চ্যানেল থেকে নয়, যদি আপনি অ্যাডমিন না হন)
        if dialog.is_group:
            print(f"\nগ্রুপ স্ক্যান করা হচ্ছে: {dialog.name}")
            
            try:
                async for user in client.iter_participants(dialog):
                    if total_added >= LIMIT:
                        print("আজকের মতো ২০০ জনের লিমিট শেষ!")
                        break
                    
                    # নিজেকে বা বটকে অ্যাড করা থেকে বিরত থাকা
                    if user.bot or user.self:
                        continue

                    try:
                        # মেম্বারকে আপনার চ্যানেলে অ্যাড করা
                        await client(InviteToChannelRequest(target_entity, [user]))
                        total_added += 1
                        print(f"{total_added}. সফলভাবে অ্যাড হয়েছে: {user.first_name}")
                        
                        # প্রতি অ্যাডের মাঝে ২০ সেকেন্ড গ্যাপ (আইডি সেফ রাখতে)
                        time.sleep(20)

                    except UserPrivacyRestrictedError:
                        print(f"ইউজার {user.id}-এর প্রাইভেসি সেটিংসের কারণে অ্যাড করা গেল না।")
                    except PeerFloodError:
                        print("টেলিগ্রাম থেকে স্প্যাম রিপোর্ট এসেছে। আজকের মতো কাজ বন্ধ রাখুন!")
                        return
                    except FloodWaitError as e:
                        print(f"অপেক্ষা করতে হবে: {e.seconds} সেকেন্ড")
                        time.sleep(e.seconds)
                    except Exception as e:
                        print(f"ছোট ভুল: {e}")
                        continue
                        
            except Exception as e:
                print(f"{dialog.name} থেকে মেম্বার লিস্ট নেওয়া সম্ভব হয়নি।")
                continue

    print(f"\nকাজ শেষ! মোট {total_added} জন মেম্বার অ্যাড করার চেষ্টা করা হয়েছে।")

with client:
    client.loop.run_until_complete(main())
