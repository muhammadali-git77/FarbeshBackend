from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Driver
import requests

from utils.env import TELEGRAM_ID,TELEGRAM_BOT_TOKEN

  
TELEGRAM_GROUP_ID = TELEGRAM_ID 

@receiver(post_save, sender=Driver)
def send_telegram_invite_link(sender, instance, **kwargs):
    if instance.payment_status:
        telegram_id = instance.telegram_id
        full_name = instance.full_name

        # Foydalanuvchi guruhda mavjudligini tekshirish
        check_member_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember"
        check_member_payload = {
            'chat_id': TELEGRAM_GROUP_ID,
            'user_id': telegram_id
        }
        response = requests.get(check_member_url, params=check_member_payload).json()

        # Agar foydalanuvchi guruhda bo'lsa, hech narsa qilinmasin
        if response.get('ok') and response['result']['status'] in ['member', 'administrator', 'creator']:
            print(f"✅ {full_name} allaqachon guruhda mavjud.")
            return

        # Foydalanuvchi guruhda mavjud bo'lmasa, taklifnoma yaratish
        expire_date = int((timezone.now() + timedelta(minutes=15)).timestamp())
        create_invite_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/createChatInviteLink"
        create_invite_payload = {
            'chat_id': TELEGRAM_GROUP_ID,
            'expire_date': expire_date,
            'member_limit': 1  # Bir martalik ishlatilishi uchun
        }
        invite_response = requests.post(create_invite_url, json=create_invite_payload).json()

        if invite_response.get('ok'):
            invite_link = invite_response['result']['invite_link']
            # Foydalanuvchiga taklifnomani yuborish
            send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            message = (
                f"👋 Assalomu alaykum, {full_name}!\n\n"
                f"✅ Sizning FarBesh haydovchilar guruhiga qo'shilish so'rovingiz qabul qilindi.\n\n"
                f"🔗 Quyidagi havola orqali guruhga qo'shiling:\n"
                f"👉 {invite_link}\n\n"
                f"⚠️ <b>Eslatma:</b>\n"
                f"• Havola faqat <b>15 daqiqa</b> amal qiladi.\n"
                f"• Havola <b>bir marta</b> ishlatilishi mumkin.\n\n"
                f"📌 <b>Guruhning maqsadi:</b>\n"
                f"Ushbu guruh orqali sizga buyurtmalar yuboriladi. "
                f"Guruhda faqat buyurtmalar va ular bilan bog'liq muhim ma'lumotlar joylashtiriladi.\n\n"
                f"📢 <b>Qo'shimcha ma'lumot:</b>\n"
                f"Agar savollaringiz bo'lsa, tizim adminlari bilan bog'lanishingiz mumkin."
            )
            send_message_payload = {
                'chat_id': telegram_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            send_response = requests.post(send_message_url, json=send_message_payload).json()

            if send_response.get('ok'):
                print(f"✅ {full_name} ga taklifnoma muvaffaqiyatli yuborildi!")
            else:
                print(f"❌ {full_name} ga xabar jo'natishda xatolik yuz berdi:", send_response)
        else:
            print(f"❌ {full_name} uchun taklifnoma yaratishda xatolik yuz berdi:", invite_response)
