# modified by @modwini
from .. import loader, utils
import telethon
import logging
import os
import time
import re
import json
import requests
import string
import io

logger = logging.getLogger(__name__)

version = "Beta v2.2.7"


@loader.tds
class InnoChatMod(loader.Module):
    """Подпишись на канал @modwini"""
    strings = {
        'name': 'InnoChat',

        'antisex_on': '🔞 <b>Антисекс вкл\nДействие: {}</b>',
        'antisex_off': '🔞 <b>Антисекс выкл</b>',
        'antisex': '🔞 <b><a href="tg://user?id={}">{}</a>, вы\'подозрительны!\nДействие: {}</b>',

        'atagall_on': '🐵 <b>AntiTagAll вкл\nДействие: {}</b>',
        'atagall_off': '🐵 <b>AntiTagAll выкл</b>',
        'tagall': '🐵 <b>Похоже вы <a href="tg://user?id={}">{}</a> используете TagAll.\n👊 Действие: I {}</b>',
        'args': '🦊 <b>Аргументы неверны</b>',
        'atagall_action_set': '🐵 <b>Действие AntiTagAll установлено на "{}"</b>',

        'as_on': '🐻 <b>Arab Shield вкл\Действие: {}</b>',
        'as_off': '🐻 <b>Arab Shield выкл</b>',
        'arabic_nickname': '🐻 <b>Похоже вы <a href="tg://user?id={}">{}</a> араб.\n👊 Действие: I {}</b>',
        'arab_action_set': '🐻 <b>Arab shield Действие установлено на "{}"</b>',

        'antihelp_on': '🐺 <b>Anti Help вкл</b>',
        'antihelp_off': '🐺 <b>Anti Help выкл</b>',

        'als_on': '🐼 <b>AntiLogspam вкл (аксимум {} за {} секунд)\nДействие: {}</b>',
        'als_off': '🐼 <b>AntiLogspam выкл</b>',
        'logspam': '🐼 <b>Похоже <a href="tg://user?id={}">{}</a> LogSpamming.\n👊 Действие: I {}</b>',
        'als_action_set': '🐼 <b>Действие ALS настроено на "{}"</b>',
        'als_range_set': '🐼 <b>Текущий предел ALS составляет {} per {}</b>',

        'ar_on': '🐶 <b>Антирейд включен\nДействие: {}</b>',
        'ar_off': '🐶 <b>Антирейд выключен</b>',
        'antiraid': '🐶 <b>Антирейд включен. I {} <a href="tg://user?id={}">{}</a> в группе {}</b>',

        'no_reason': 'Без причины',
        'warn': '👮‍♂️ <b><a href="tg://user?id={}">{}</a></b> получил {}/{} предупреждение\nПричина: <b>{}</b>',
        'fwarn': '👮‍♂️💼 <b><a href="tg://user?id={}">{}</a></b> получил {}/{} федеративное предупреждение\nПричина: <b>{}</b>',
        'chat_not_in_db': '👮‍♂️ <b>В этом чате пока нет предупреждений</b>',
        'no_fed_warns': '👮‍♂️ <b>У этой федерации пока нет предупреждений</b>',
        'no_warns': '👮‍♂️ <b><a href="tg://user?id={}">{}</a> пока нет предупреждений</b>',
        'warns': '👮‍♂️ <b><a href="tg://user?id={}">{}</a> имеет {}/{} предупреждений</b>\n    🏴󠁧󠁢󠁥󠁮󠁧󠁿 <i>{}</i>',
        'warns_adm': '👮‍♂️ <b>Предупреждения в этом чате</b>:\n',
        'warns_adm_fed': '👮‍♂️ <b>Предупреждения в этой федерации</b>:\n',
        'dwarn': '👮‍♂️ <b>Удалено последнее предупреждение из <a href="tg://user?id={}">{}</a></b>',
        'dwarn_fed': '👮‍♂️ <b>Удалено последнее федеративное предупреждение из <a href="tg://user?id={}">{}</a></b>',
        'clrwarns': '👮‍♂️ <b>Убраны все предупреждения из <a href="tg://user?id={}">{}</a></b>',
        'clrwarns_fed': '👮‍♂️ <b>Удалены все федеративные предупреждения из <a href="tg://user?id={}">{}</a></b>',
        'new_a': '👮‍♂️ <b>Новое действие при достижении предела предупреждений для этого чата: "{}"</b>',
        'new_l': '👮‍♂️ <b>Новое действие при достижении предела предупреждений для этой федерации: "{}"</b>',
        'warns_limit': '👮‍♂️ <b><a href="tg://user?id={}">{}</a> достигнут лимит предупреждений.\nДействие: I {}</b>',

        'welcome': '👋 <b>Теперь я буду приветствовать людей в этом чате</b>',
        'chat_not_found': '👋 <b>Я пока не приветствую людей в этом чате</b>',
        'unwelcome': '👋 <b>Теперь я не буду приветствовать людей в этом чате</b>',

        'chat404': '🦊 <b>Я еще не защищаю этот чат.</b>\n',
        'protections': '<b>🐻 AntiArab:</b> <code>.antiarab</code>\n<b>🐼 AntiLogspam:</b> <code>.als</code> <code>.alsset</code>\n<b>🐺 AntiHelp:</b> <code>.antihelp</code>\n<b>🐵 AntiTagAll:</b> <code>.atagall</code>\n<b>👋 Welcome: </b><code>.welcome</code>\n<b>🐶 AntiRaid:</b> <code>.antiraid</code>\n<b>🔞 AntiSex:</b> <code>.antisex</code>\n<b>📯 AntiChannel:</b> <code>.antichannel</code>\n<b>🪙 AntiSpoiler:</b> <code>.antispoiler</code>\n<b>🍓 AntiNSFW:</b> <code>.antinsfw</code>\n<b>⏱ AntiFlood:</b> <code>.antiflood</code>\n<b>👾 Admin: </b>\n<code>.ban</code> <code>.kick</code> <code>.mute</code>\n<code>.unban</code> <code>.unmute</code>\n<code>.def</code> <code>.gdef</code> <code>.deflist</code> <code>.gdeflist</code>\n<b>👮‍♂️ Warns:</b> <code>.warn</code> <code>.warns</code> <code>.warnslimit</code>\n<code>.dwarn</code> <code>.clrwarns</code> <code>.warnsaciton</code>\n<b>💼 Federations:</b> <code>.fadd</code> <code>.frm</code> <code>.newfed</code>\n <code>.namefed</code> <code>.fban</code> <code>.rmfed</code> <code>.feds</code>',

        'prefix_set': '👾 <b><a href="tg://user?id={}">{}</a></b>\'префикс теперь <b>{}</b>',
        'prefix_removed': '👾 <b><a href="tg://user?id={}">{}</a> теперь без префикса</b>',
        'not_admin': '👾 <b>Я здесь не администратор или у меня недостаточно прав</b>',
        'mute': '👾 <b><a href="tg://user?id={}">{}</a> получил мут {}. Причина: {}</b>',
        'ban': '👾 <b><a href="tg://user?id={}">{}</a> забанен {}. Причина: {}</b>',
        'kick': '👾 <b><a href="tg://user?id={}">{}</a> кикнут Причина: {}</b>',
        'unmuted': '👾 <b><a href="tg://user?id={}">{}</a> теперь может писать</b>',
        'unban': '👾 <b><a href="tg://user?id={}">{}</a> разблокирован</b>',

        'defense': '🛡 <b>Щит для <a href="tg://user?id={}">{}</a> теперь {}</b>',
        'no_defense': '🛡 <b>I не защищать пользователей в этом чате прямо сейчас</b>',
        'defense_list': '🛡 <b>Неуязвимые пользователи в текущем чате:</b>\n{}',

        'antichannel': '📯 <b>AntiChannel теперь {} в этом чате</b>',
        'antiflood': '⏱ <b>AntiFlood теперь {} в этом чате\nДействие: {}</b>',
        'flood': '⏱ <b>Похоже на <a href="tg://user?id={}">{}</a> флуд.\n👊 Действие: I {}</b>',
        'antispoiler': '🪙 <b>AntiSpoiler теперь {} в этом чате</b>',

        'nsfw_toggle': '🍓 <b>AntiNSFW теперь {} в этом чате</b>',
        'nsfw_content': '🍓 <b>Похоже на <a href="tg://user?id={}">{}</a> отправил NSFW-контент.\n👊 Действие: I {}</b>',

        'fadded': '💼 <b> этот чат добавлен в федерацию "{}"</b>',
        'newfed': '💼 <b>Созданна федерация "{}"</b>',
        'rmfed': '💼 <b>Созданная федерация "{}"</b>',
        'fed404': '💼 <b>Федерация не найдена</b>',
        'frem': '💼 <b>Текущий чат удален из федерации "{}"</b>',
        'f404': '💼 <b>Текущий чат не в федерации "{}"</b>',
        'fexists': '💼 <b>Текущий чат уже в федерации "{}"</b>',
        'fedexists': '💼 <b>Федерация существует</b>',
        'namedfed': '💼 <b>Федерация переименована в {}</b>',
        'nofed': '💼 <b>Текущий чат не принадлежит ни к одной федерации</b>',
        'fban': '💼 <b><a href="tg://user?id={}">{}</a> заблокирован в федерации {}\nПричина: {}</b>',
        'feds_header': '💼 <b>Федерации:</b>\n\n'
    }



    async def newfedcmd(self, message):
        """<shortname> <name> - Создать новую федерацию"""
        args = utils.get_args_raw(message)
        if not args or args.count(' ') == 0:
            return await utils.answer(message, self.strings('args'))

        shortname, name = args.split(maxsplit=1)
        if shortname in self.federations:
            return await utils.answer(message, self.strings('fedexists'))

        self.federations[shortname] = {
            'name': name,
            'chats': [],
            'warns': {}
        }

        self.db.set('InnoChats', 'federations', self.federations)

        await utils.answer(message, self.strings('newfed').format(name))


    async def rmfedcmd(self, message):
        """<короткое имя> - с"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings('args'))

        if args not in self.federations:
            return await utils.answer(message, self.strings('fed404'))

        name = self.federations[args]['name']

        del self.federations[args]
        self.db.set('InnoChats', 'federations', self.federations)

        await utils.answer(message, self.strings('rmfed').format(name))


    async def namefedcmd(self, message):
        """<shortname> <name> — переименовать федерацию"""
        args = utils.get_args_raw(message)
        if not args or args.count(' ') == 0:
            return await utils.answer(message, self.strings('args'))

        shortname, name = args.split(maxsplit=1)

        if shortname not in self.federations:
            return await utils.answer(message, self.strings('fed404'))

        self.federations[shortname]['name'] = name
        self.db.set('InnoChats', 'federations', self.federations)
        await utils.answer(message, self.strings('namedfed').format(name))


    async def faddcmd(self, message):
        """<fed name> — добавить чат в федерацию"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings('args'))

        if args not in self.federations:
            return await utils.answer(message, self.strings('fed404'))

        chat = utils.get_chat_id(message)

        if chat in self.federations[args]['chats']:
            return await utils.answer(message, self.strings('fexists').format(self.federations[args]['name']))

        self.federations[args]['chats'] += [chat]

        self.db.set('InnoChats', 'federations', self.federations)

        await utils.answer(message, self.strings('fadded').format(self.federations[args]['name']))


    async def frmcmd(self, message):
        """<fed name> - Удалить чат из федерации"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings('args'))

        if args not in self.federations:
            return await utils.answer(message, self.strings('fed404'))

        chat = utils.get_chat_id(message)

        if chat not in self.federations[args]['chats']:
            return await utils.answer(message, self.strings('f404').format(self.federations[args]['name']))

        self.federations[args]['chats'].remove(chat)

        self.db.set('InnoChats', 'federations', self.federations)

        await utils.answer(message, self.strings('frem').format(self.federations[args]['name']))



    @loader.sudo
    async def fbancmd(self, message):
        """<reply | user> <reason | optional> - Забанить пользователя в федерации"""
        cid = utils.get_chat_id(message)
        fed = None
        for federation, config in self.federations.items():
            if cid in config['chats']:
                fed = federation
                break

        if not fed:
            return await utils.answer(message, self.strings('no_fed'))

        if message.is_private:
            await message.delete()
            return

        a = await self.args_parser_2(message)
        if not a:
            return await utils.answer(message, self.strings('args'))

        user, t, reason = a

        for c in self.federations[fed]['chats']:
            try:
                chat = await self.client.get_entity(c)
            except Exception:
                continue

            if not chat.admin_rights and not chat.creator:
                continue

            try:
                await self.client.edit_permissions(chat, user, until_date=time.time() + t, view_messages=False,
                                                   send_messages=False, send_media=False, send_stickers=False,
                                                   send_gifs=False, send_games=False, send_inline=False, send_polls=False,
                                                   change_info=False, invite_users=False)
                if chat.id != cid: await self.client.send_message(chat, self.strings('ban', message).format(user.id,
                                                                                user.first_name if getattr(user,
                                                                                                           'first_name',
                                                                                                           None) is not None else user.title,
                                                                                f'for {t//60} min(-s)' if t != 0 else 'forever',
                                                                                reason))
            except telethon.errors.UserAdminInvalidError:
                pass

        await utils.answer(message, self.strings('fban').format(user.id, user.first_name if getattr(user,
                                                                                                           'first_name',
                                                                                                           None) is not None else user.title,
                                                                    self.federations[fed]['name'], reason))




    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.me = str((await client.get_me()).id)
        self.chats = db.get('InnoChats', 'chats', {})
        self.warns = db.get('InnoChats', 'warns', {})
        self.federations = db.get('InnoChats', 'federations', {})
        self.flood_timeout = 4
        self.flood_threshold = 4
        try:
            self.cache = json.loads(open('als_cache.json', 'r').read())
        except Exception:
            self.cache = {}

        try:
            self.flood_cache = json.loads(open('flood_cache.json', 'r').read())
        except Exception:
            self.flood_cache = {}

        self.correction = 1636106678
        self.token = db.get('InnoChats', 'apitoken', False)

        async def deleted_handler(event):
            for msid in event.deleted_ids:
                try:
                    cid = str(event.original_update.channel_id)
                except AttributeError:
                    return

                if cid + '_' + str(msid) not in self.cache: return

                try:
                    user = str(self.cache[cid + '_' + str(msid)][0])
                except Exception:
                    return

                if cid not in self.chats: return

                await self.check_user(cid, user, 'deleted')

        async def edited_handler(event):
            cid = str(utils.get_chat_id(event.message))
            user = str(event.message.sender_id)
            await self.check_user(cid, user, 'edited', event)

        try:
            client.remove_event_handler(
                loader.logspam_edit_handler, telethon.events.MessageEdited())
        except Exception:
            pass

        loader.logspam_edit_handler = edited_handler

        await self.update_handlers()


    def ctime(self, t):
        if 'h' in str(t): t = int(t[:-1]) * 60 * 60
        if 'm' in str(t): t = int(t[:-1]) * 60
        if 's' in str(t): t = int(t[:-1])
        try:
            t = int(t)
        except Exception: pass

        return t

    async def args_parser_1(self, message):
        """Получить аргументы из сообщения
        пользователь | время | причина"""
        t = message.raw_text
        try:
            args = t.split(maxsplit=1)[1]
        except Exception:
            args = ""

        reply = await message.get_reply_message()

        # .ban <reply>
        try:
            if not args and reply:
                user = await self.client.get_entity(reply.sender_id)
                t = 0
                reason = self.strings('no_reason')
                return user, t, reason
        except Exception as e: logger.exception(e)

        # .ban <user>

        try:
            if not reply and args:
                user = await self.client.get_entity(args)
                t = 0
                reason = self.strings('no_reason')
                return user, t, reason
        except Exception as e: logger.exception(e)

        # .ban <time> <reply>

        try:
            if reply and self.ctime(args):
                user = await self.client.get_entity(args)
                t = self.ctime(args)
                reason = self.strings('no_reason')
                return user, t, reason
        except Exception as e: logger.exception(e)

        # .ban <time> <user> [reason]

        try:
            if not reply and args:
                a = args.split(maxsplit=2)
                t = self.ctime(a[0])
                user = await self.client.get_entity(a[1])
                reason = ' '.join(a[2:]) if len(a) > 2 else self.strings('no_reason')
                return user, t, reason
        except Exception as e: logger.exception(e)

        # .ban <time> <reason>

        try:
            if reply and args:
                a = args.split(maxsplit=2)
                t = self.ctime(a[0])
                user = await self.client.get_entity(reply.from_id)
                reason = a[1] or self.strings('no_reason')
                return user, t, reason
        except Exception as e: logger.exception(e)


        return False

    async def args_parser_2(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user = None
        if not reply:
            try:
                user, reason = args.split(maxsplit=1)
                user = await self.client.get_entity(user)
                reason = reason or self.strings('no_reason')
                t = 0
            except Exception:
                pass

            if not user:
                try:
                    user = await self.client.get_entity(user)
                except Exception:
                    return await utils.answer(message, self.strings('args'))

                reason = args or self.strings('no_reason')
                t = 0
        else:
            user = await self.client.get_entity(reply.sender_id)
            reason = args or self.strings('no_reason')
            t = 0

        return user, t, reason




    @loader.group_admin_ban_users
    async def kickcmd(self, message):
        """ответить | пользователь> <причина | необязательно> - Выгнать пользователя"""
        chat = await message.get_chat()
        if message.is_private:
            await message.delete()
            return

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings('not_admin'))

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        user, reason = None, None

        try:
            if reply:
                user = await self.client.get_entity(reply.sender_id)
                reason = args if args else self.strings('no_reason')
            else:
                uid = args.split(maxsplit=1)[0]
                try:
                    uid = int(uid)
                except Exception:
                    pass
                user = await self.client.get_entity(uid)
                reason = args.split(maxsplit=1)[1] if len(
                    args.split(maxsplit=1)) > 1 else self.strings('no_reason')
        except Exception:
            await utils.answer(message, self.strings('args', message))
            return

        try:
            await self.client.kick_participant(utils.get_chat_id(message), user)
            await utils.answer(message, self.strings('kick', message).format(user.id, user.first_name if getattr(user,
                                                                                                                 'first_name',
                                                                                                                 None) is not None else user.title,
                                                                             reason))
        except telethon.errors.UserAdminInvalidError:
            await utils.answer(message, self.strings('not_admin', message))
            return

    @loader.group_admin_ban_users
    async def bancmd(self, message):
        """<ответить | пользователь> <причина | необязательно> - Забанить пользователя"""
        chat = await message.get_chat()
        if message.is_private:
            await message.delete()
            return

        a = await self.args_parser_2(message)
        if not a:
            return await utils.answer(message, self.strings('args'))

        user, t, reason = a

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings('not_admin', message))

        try:
            await self.client.edit_permissions(chat, user, until_date=time.time() + t, view_messages=False,
                                               send_messages=False, send_media=False, send_stickers=False,
                                               send_gifs=False, send_games=False, send_inline=False, send_polls=False,
                                               change_info=False, invite_users=False)
            await utils.answer(message, self.strings('ban', message).format(user.id,
                                                                            user.first_name if getattr(user,
                                                                                                       'first_name',
                                                                                                       None) is not None else user.title,
                                                                            f'for {t//60} min(-s)' if t != 0 else 'forever',
                                                                            reason))
        except telethon.errors.UserAdminInvalidError:
            await utils.answer(message, self.strings('not_admin', message))
            return

    @loader.group_admin_ban_users
    async def mutecmd(self, message):
        """<ответить | пользователь> <время | 0 для бесконечности> <причина | необязательно> - замутить пользователя"""
        chat = await message.get_chat()
        if message.is_private:
            await message.delete()
            return

        a = await self.args_parser_1(message)
        if not a:
            return await utils.answer(message, self.strings('args'))

        user, t, reason = a

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings('not_admin', message))

        try:
            await self.client.edit_permissions(chat, user, until_date=time.time() + t, send_messages=False)
            await utils.answer(message, self.strings('mute', message).format(user.id, user.first_name if getattr(user,
                                                                                                                 'first_name',
                                                                                                                 None) is not None else user.title,
                                                                             f'for {t//60} min(-s)' if t != 0 else 'forever',
                                                                             reason))
        except telethon.errors.UserAdminInvalidError:
            await utils.answer(message, self.strings('not_admin', message))
            return

    @loader.group_admin_ban_users
    async def unmutecmd(self, message):
        """ответить | пользователь> - размутить пользователя"""
        chat = await message.get_chat()
        if message.is_private:
            await message.delete()
            return

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings('not_admin', message))

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        user = None

        try:
            try:
                args = int(args)
            except Exception: pass
            user = await self.client.get_entity(args)
        except Exception:
            await utils.answer(message, self.strings('args', message))
            return

        if not user:
            try:
                user = await self.client.get_entity(reply.sender_id)
            except Exception:
                return await utils.answer(message, self.strings('args'))

        try:
            await self.client.edit_permissions(chat, user, until_date=0, send_messages=True)
            await utils.answer(message,
                               self.strings('unmuted', message).format(user.id, user.first_name if getattr(user,
                                                                                                           'first_name',
                                                                                                           None) is not None else user.title))
        except telethon.errors.UserAdminInvalidError:
            await utils.answer(message, self.strings('not_admin', message))
            return

    @loader.group_admin_ban_users
    async def unbancmd(self, message):
        """<ответить | user> - Разблокировать пользователя"""
        chat = await message.get_chat()
        if message.is_private:
            await message.delete()
            return

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings('not_admin', message))

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        user = None

        try:
            try:
                args = int(args)
            except Exception: pass
            user = await self.client.get_entity(args)
        except Exception:
            pass

        if not user:
            try:
                user = await self.client.get_entity(reply.sender_id)
            except Exception:
                return await utils.answer(message, self.strings('args'))


        try:
            await self.client.edit_permissions(chat, user, until_date=0, view_messages=True, send_messages=True,
                                               send_media=True, send_stickers=True, send_gifs=True, send_games=True,
                                               send_inline=True, send_polls=True, change_info=True, invite_users=True)
            await utils.answer(message, self.strings('unban', message).format(user.id, user.first_name if getattr(user,
                                                                                                                  'first_name',
                                                                                                                  None) is not None else user.title))
        except telethon.errors.UserAdminInvalidError:
            await utils.answer(message, self.strings('not_admin', message))
            return

    @loader.group_owner
    async def antisexcmd(self, message):
        """мут | бан | кик | нет, чтобы отключить> - Включить антисекс"""

        chat = str(utils.get_chat_id(message))
        args = utils.get_args_raw(message)

        if chat not in self.chats:
            self.chats[chat] = {}

        if args in ['mute', 'ban', 'kick']:
            self.chats[chat]['antisex'] = args
            await utils.answer(message, self.strings('antisex_on', message).format(args))
        else:
            if 'antisex' in self.chats[chat]:
                del self.chats[chat]['antisex']
            await utils.answer(message, self.strings('antisex_off', message))

        self.db.set('InnoChats', 'chats', self.chats)

    @loader.group_owner
    async def antiraidcmd(self, message):
        """<мут | бан | кик | нет для отключения> - Включить антирейд"""

        chat = str(utils.get_chat_id(message))
        args = utils.get_args_raw(message)

        if chat not in self.chats:
            self.chats[chat] = {}

        if args in ['mute', 'ban', 'kick']:
            self.chats[chat]['antiraid'] = args
            await utils.answer(message, self.strings('ar_on', message).format(args))
        else:
            if 'antiraid' in self.chats[chat]:
                del self.chats[chat]['antiraid']
            await utils.answer(message, self.strings('ar_off', message))

        self.db.set('InnoChats', 'chats', self.chats)

    @loader.group_owner
    async def atagallcmd(self, message):
        """Переключить AntiTagAll"""

        chat = str(utils.get_chat_id(message))
        if chat not in self.chats:
            self.chats[chat] = {}

        if args not in ['warn', 'ban', 'kick', 'mute', 'delmsg']:
            if 'antitagall' in self.chats[chat]:
                del self.chats[chat]['antitagall']
                await utils.answer(message, self.strings('atagall_off'))
        else:
            self.chats[chat]['antitagall'] = args
            await utils.answer(message, self.strings('atagall_on').format(args))

        self.db.set('InnoChats', 'chats', self.chats)

    @loader.group_owner
    async def antihelpcmd(self, message):
        """Переключить антипомощь"""

        chat = str(utils.get_chat_id(message))
        if chat not in self.chats:
            self.chats[chat] = {}

        if 'antihelp' not in self.chats[chat]:
            self.chats[chat]['antihelp'] = True
            await utils.answer(message, self.strings('antihelp_on', message).format('mute'))
        else:
            del self.chats[chat]['antihelp']
            await utils.answer(message, self.strings('antihelp_off', message))

        self.db.set('InnoChats', 'chats', self.chats)

    @loader.group_owner
    async def antiarabcmd(self, message):
        """Переключить антиарабский язык"""
        chat = str(utils.get_chat_id(message))
        if chat not in self.chats:
            self.chats[chat] = {}

        args = utils.get_args_raw(message)

        if args not in ['warn', 'ban', 'kick', 'mute', 'delmsg']:
            if 'arabshield' in self.chats[chat]:
                del self.chats[chat]['arabshield']
            await utils.answer(message, self.strings('as_off'))
        else:
            self.chats[chat]['arabshield'] = args
            await utils.answer(message, self.strings('as_on').format(args))

        self.db.set('InnoChats', 'chats', self.chats)


    @loader.group_owner
    async def alscmd(self, message):
        """Переключить LogSpam"""

        chat = str(utils.get_chat_id(message))
        if chat not in self.chats:
            self.chats[chat] = {}

        args = utils.get_args_raw(message)

        if args not in ['warn', 'ban', 'kick', 'mute', 'delmsg', 'nothing']:
            args = False

        if args:
            self.chats[chat]['als'] = {'settings': 
                {
                    'cooldown': 0,
                    'detection_range': 10,
                    'detection_interval': 10,
                    'action': args
                }
            }
            await utils.answer(message, self.strings('als_on', message).format(
                self.chats[chat]['als']['settings']['detection_range'],
                self.chats[chat]['als']['settings']['detection_interval'],
                self.chats[chat]['als']['settings']['action']))
        else:
            if 'als' in self.chats[chat]:
                del self.chats[chat]['als']
            await utils.answer(message, self.strings('als_off', message))

        self.db.set('InnoChats', 'chats', self.chats)
        await self.update_handlers()


    @loader.group_owner
    async def alssetcmd(self, message):
        """<limit> <time sample> - установить лимит и образец времени"""

        args = utils.get_args_raw(message)
        chat = str(utils.get_chat_id(message))
        if not args or len(args.split()) != 2:
            await utils.answer(message, self.strings('args', message))
            return

        try:
            limit, time_sample = list(map(int, args.split()))
        except Exception:
            await utils.answer(message, self.strings('args', message))
            return

        if chat not in self.chats:
            self.chats[chat] = {}

        if 'als' not in self.chats[chat]:
            self.chats[chat]['als'] = {}

        if 'settings' not in self.chats[chat]['als']:
            self.chats[chat]['als']['settings'] = {
                'cooldown': 0,
                'detection_range': 10,
                'detection_interval': 10,
                'action': 'delmsg'
            }

        self.chats[chat]['als']['settings']['detection_range'], self.chats[chat]['als']['settings'][
            'detection_interval'] = limit, time_sample
        self.db.set('InnoChats', 'chats', self.chats)
        await utils.answer(message, self.strings('als_range_set', message).format(limit, time_sample))

    @loader.group_owner
    async def update_handlers(self):
        try:
            try:
                self.client.remove_event_handler(
                    loader.logspam_edit_handler, telethon.events.MessageEdited())
            except Exception: pass
            self.client.add_event_handler(
                loader.logspam_edit_handler, telethon.events.MessageEdited(incoming=True))
    
        except Exception:
            return

    @loader.group_owner
    async def check_user(self, cid, user, event_type, event=None):
        if cid in self.chats and self.chats[cid] and 'defense' in self.chats[cid] and self.chats[cid][
            'defense'] and user in self.chats[cid]['defense']:
            return

        if user == self.me:
            return

        if cid not in self.chats:
            return

        if 'als' not in self.chats[cid]:
            return

        changes = False
        if user not in self.chats[cid]['als']:
            self.chats[cid]['als'][user] = []
            changes = True

        self.chats[cid]['als'][user].append(round(time.time()))

        for u, timings in self.chats[cid]['als'].items():
            if u == 'settings':
                continue
            loc_timings = timings.copy()
            for timing in loc_timings:
                if timing + self.chats[cid]['als']['settings']['detection_interval'] <= time.time():
                    self.chats[cid]['als'][u].remove(timing)
                    changes = True

        if len(self.chats[cid]['als'][user]) >= self.chats[cid]['als']['settings']['detection_range']:
            action = self.chats[cid]['als']['settings']['action']
            if event_type != 'deleted':
                try:
                    await event.message.delete()
                except Exception: pass

            if int(self.chats[cid]['als']['settings']['cooldown']) <= time.time():
                try:
                    user_name = (await self.client.get_entity(int(user))).first_name
                except Exception:
                    user_name = "Brother"

                await self.punish(int(cid), int(user), 'logspam',
                                  self.chats[cid]['als']['settings']['action'], user_name)

                self.chats[cid]['als']['settings']['cooldown'] = round(
                    time.time()) + 15

            del self.chats[cid]['als'][user]
            changes = True

        if changes:
            self.db.set('InnoChats', 'chats', self.chats)


    @loader.group_owner
    async def protectscmd(self, message):
        """Список доступных фильтров"""
        await utils.answer(message, self.strings('protections', message))


    async def fedscmd(self, message):
        """Список федераций"""
        res = self.strings('feds_header')
        for shortname, config in self.federations.copy().items():
            res += f"    ☮️ <b>{config['name']}</b> (<code>{shortname}</code>)"
            for chat in config['chats'].copy():
                try:
                    c = await self.client.get_entity(chat)
                except Exception:
                    self.federations[shortname]['chats'].remove(chat)
                    continue

                res += f"\n        <b>- <a href=\"tg://resolve?domain={c.username if getattr(c, 'username', None) is not None else ''}\">{c.title}</a></b>"

            res += f"\n        <b>👮‍♂️ {len(config['warns'])} предупреждение</b>"

        await utils.answer(message, res)


    async def pchatscmd(self, message):
        """Список средств защиты"""

        res = f"<b><u>🦊 @modwini Список защиты </u></b> <i>{version}</i>\n\n<i>🐼 - AntiLogspam\n🐺 - AntiHelp\n🐻 - AntiArab\n🐵 - AntiTagAll\n💋 - AntiSex\n🚪 - AntiRaid\n📯 - AntiChannel\n🪙 - AntiSpoiler\n🍓 - AntiNSFW\n⏱ - AntiFlood\n\n👋 - Welcome\n👮‍♂️ - Local warns\n💼 - Federations</i>\n\n🦊 <b><u>Chats:</u></b>\n"
        changes = False
        for chat, obj in self.chats.copy().items():
            try:
                chat_obj = await self.client.get_entity(int(chat))
                if getattr(chat_obj, 'title', False):
                    chat_name = chat_obj.title
                else:
                    chat_name = chat_obj.first_name
            except Exception:
                del self.chats[chat]
                changes = True
                continue

            fed = None
            for federation, config in self.federations.items():
                if int(cid) in config['chats']:
                    fed = federation
                    break

            line = ""
            line += "🐼" if 'als' in obj else ""
            line += "🐺" if 'antihelp' in obj else ""
            line += "🐻" if 'arabshield' in obj else ""
            line += "🐵" if 'antitagall' in obj else ""
            line += "💋" if 'antisex' in obj else ""
            line += "🚪" if 'antiraid' in obj else ""
            line += "🪙" if 'antispoiler' in obj else ""
            line += "📯" if 'antichannel' in obj else ""
            line += "🍓" if 'antinsfw' in obj else ""
            line += "⏱" if 'antiflood' in obj else ""
            line += "👋" if 'welcome' in obj else ""
            line += "👮‍♂️" if chat in self.warns else ""
            line += "💼" if fed is not None else ""

            if not line:
                del self.chats[chat]
                changes = True
                continue

            res += "<code>    </code>◾️ " + chat_name + ": " + line + "\n"

        if changes:
            self.db.set('InnoChats', 'chats', self.chats)

        await utils.answer(message, res)

    @loader.group_owner
    async def pchatcmd(self, message):
        """Список защиты для текущего чата
"""

        cid = str(utils.get_chat_id(message))

        if cid not in self.chats or not self.chats[cid]:
            return await utils.answer(message, self.strings('chat404', message))

        res = f"<b><u>🦊 @modwini Защита чата</u></b> <i>{version}</i>\n"

        obj = self.chats[cid]

        fed = None
        for federation, config in self.federations.items():
            if int(cid) in config['chats']:
                fed = federation
                break

        line = ""
        line += "\n🐺 <b>AntiHelp.</b>" if 'antihelp' in obj else ""
        line += "\n🐵 <b>AntiTagAll.</b> Действие: <b>{}</b>".format(
            obj['antitagall']) if 'antitagall' in obj else ""
        line += "\n🐻 <b>AntiArab.</b> Действие: <b>{}</b>".format(
            obj['arabshield']) if 'arabshield' in obj else ""

        line += "\n🐼 <b>AntiLogspam.</b> Действие: <b>{}</b> if <b>{}</b> per <b>{}s</b>".format(
            obj['als']['settings']['Действие'], obj['als']['settings']['detection_range'],
            obj['als']['settings']['detection_interval']) if 'als' in obj else ""
        line += "\n💋 <b>AntiSex</b> Действие: <b>{}</b>".format(obj['antisex']) if 'antisex' in obj else ""
        line += "\n🚪 <b>AntiRaid</b> Действие: <b>{} кто присоединилися</b>".format(obj['antiraid']) if 'antiraid' in obj else ""
        line += "\n📯 <b>AntiChannel.</b>" if 'antichannel' in obj else ""
        line += "\n🪙 <b>AntiSpoiler.</b>" if 'antispoiler' in obj else ""
        line += "\n🍓 <b>AntiNSFW.</b>" if 'antinsfw' in obj else ""
        line += "\n⏱ <b>AntiFlood</b> Действие: <b>{}</b>".format(obj['antiflood']) if 'antiflood' in obj else ""
        line += "\n👋 <b>Welcome.</b> \n<code>    </code>{}".format(
            obj['welcome'].replace('\n', '\n<code>    </code>')) if 'welcome' in obj else ""
        line += "\n👮‍♂️ <b>Local warns.</b>" if cid in self.warns else ""
        line += "\n💼 <b>Federation: </b>" + self.federations[fed]['name'] if fed is not None else ""

        res += line

        await utils.answer(message, res)

    async def punish(self, cid, user, violation, action, user_name):

        self.warn = ('warn' in self.allmodules.commands)

        if action == "delmsg":
            await self.client.send_message(cid, self.strings(violation).format(user, user_name, 'Удалил сообщение'))
        elif action == "kick":
            await self.client.send_message(cid, self.strings(violation).format(user, user_name, 'кикнул его'))
            await self.client.kick_participant(cid, user)
        elif action == "ban":
            await self.client.send_message(cid,
                                           self.strings(violation).format(user, user_name, 'забанил его на 1 час'))
            await self.client(telethon.tl.functions.channels.EditBannedRequest(cid, user,
                                                                               telethon.tl.types.ChatBannedRights(
                                                                                   until_date=time.time() + 60 * 60,
                                                                                   view_messages=True,
                                                                                   send_messages=True, send_media=True,
                                                                                   send_stickers=True, send_gifs=True,
                                                                                   send_games=True, send_inline=True,
                                                                                   embed_links=True)))
        elif action == "mute":
            await self.client.send_message(cid, self.strings(violation).format(user, user_name, 'заглушил его на 1 час'))
            await self.client(telethon.tl.functions.channels.EditBannedRequest(cid, user,
                                                                               telethon.tl.types.ChatBannedRights(
                                                                                   until_date=time.time() + 60 * 60,
                                                                                   send_messages=True)))
        elif action == "warn":
            if not self.warn:
                await self.client.send_message(cid, self.strings(violation).format(user, user_name,
                                                                                   'должен был его предупредить, но Warns не установлен'))
            else:
                warn_msg = await self.client.send_message(cid, f'.warn {user} {violation}')
                await self.allmodules.commands['warn'](warn_msg)
                await self.client.send_message(cid, self.strings(violation).format(user, user_name, 'предупредил его'))
        else:
            await self.client.send_message(cid, self.strings(violation).format(user, user_name, 'просто расслабься 😶‍🌫️ '))


    def save_cache(self):
        open('als_cache.json', 'w').write(json.dumps(self.cache))


    def save_flood_cache(self):
        open('flood_cache.json', 'w').write(json.dumps(self.flood_cache))


    @loader.group_admin_ban_users
    async def warncmd(self, message):
        """<ответить | айди | имя пользователя> <причина | необязательно> - Предупредить пользователя"""
        if message.is_private:
            await message.delete()
            return

        chat = await message.get_chat()

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings('not_admin'))

        cid = utils.get_chat_id(message)
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self.client.get_entity(reply.sender_id)
            if args:
                reason = args
            else:
                reason = self.strings('no_reason')
        else:
            try:
                u = args.split(maxsplit=1)[0]
                try:
                    u = int(u)
                except Exception:
                    pass

                user = await self.client.get_entity(u)
            except IndexError:
                return await utils.answer(message, self.strings('args', message))

            try:
                reason = args.split(maxsplit=1)[1]
            except IndexError:
                reason = self.strings('no_reason')


        fed = None
        for federation, config in self.federations.items():
            if cid in config['chats']:
                fed = federation
                break


        if not fed:
            if cid not in self.warns:
                self.warns[cid] = {
                    'a': 'mute',
                    'l': 5,
                    'w': {}
                }

            if str(user.id) not in self.warns[cid]['w']:
                self.warns[cid]['w'][str(user.id)] = []
            self.warns[cid]['w'][str(user.id)].append(reason)

            if len(self.warns[cid]['w'][str(user.id)]) >= self.warns[cid]['l']:
                action = self.warns[cid]['a']
                user_name = user.first_name if getattr(user, 'first_name', None) is not None else user.title
                user = user.id
                if action == "kick":
                    await self.client.kick_participant(int(cid), int(user))
                    await self.client.send_message(int(cid),
                                                   self.strings('warns_limit').format(user, user_name, 'kicked him'))
                elif action == "ban":
                    await self.client(telethon.tl.functions.channels.EditBannedRequest(int(cid), int(user),
                                                                                       telethon.tl.types.ChatBannedRights(
                                                                                           until_date=time.time() + 60 * 60,
                                                                                           view_messages=True,
                                                                                           send_messages=True,
                                                                                           send_media=True,
                                                                                           send_stickers=True,
                                                                                           send_gifs=True, send_games=True,
                                                                                           send_inline=True,
                                                                                           embed_links=True)))
                    await self.client.send_message(int(cid), self.strings('warns_limit').format(user, user_name,
                                                                                                'забанил его на 1 час'))
                elif action == "mute":
                    await self.client(telethon.tl.functions.channels.EditBannedRequest(int(cid), int(user),
                                                                                       telethon.tl.types.ChatBannedRights(
                                                                                           until_date=time.time() + 60 * 60,
                                                                                           send_messages=True)))
                    await self.client.send_message(int(cid), self.strings('warns_limit').format(user, user_name,
                                                                                                'заглушил его на 1 час'))

                await message.delete()
                self.warns[cid]['w'][str(user)] = []
            else:
                await utils.answer(message, self.strings('warn', message).format(user.id, user.first_name if getattr(user,
                                                                                                                     'first_name',
                                                                                                                     None) is not None else user.title,
                                                                                 len(self.warns[cid]['w'][str(user.id)]),
                                                                                 self.warns[cid]['l'], reason))
            self.db.set('InnoChats', 'warns', self.warns)
        else:
            if str(user.id) not in self.federations[fed]['warns']:
                self.federations[fed]['warns'][str(user.id)] = []
            self.federations[fed]['warns'][str(user.id)].append(reason)

            if len(self.federations[fed]['warns'][str(user.id)]) >= 7:
                user_name = user.first_name if getattr(user, 'first_name', None) is not None else user.title
                user = user.id
                for c in self.federations[fed]['chats']:
                    await self.client(telethon.tl.functions.channels.EditBannedRequest(c, user,
                                                                                       telethon.tl.types.ChatBannedRights(
                                                                                           until_date=time.time() + 60 * 60 * 24,
                                                                                           send_messages=True)))
                    await self.client.send_message(c, self.strings('warns_limit').format(user, user_name,
                                                                                                'заглушил его в федерации на 24 часа'))

                await message.delete()

                self.federations[fed]['warns'][str(user)] = []
            else:
                await utils.answer(message, self.strings('fwarn', message).format(user.id, user.first_name if getattr(user,
                                                                                                                     'first_name',
                                                                                                                     None) is not None else user.title,
                                                                                 len(self.federations[fed]['warns'][user.id]),
                                                                                 7, reason))
            self.db.set('InnoChats', 'federations', self.federations)


    @loader.unrestricted
    async def warnscmd(self, message):
        """<ответить | айди | имя пользователя | необязательно> - Показывать предупреждения в чате\пользователя"""
        if message.is_private:
            await message.delete()
            return

        cid = utils.get_chat_id(message)

        fed = None
        for federation, config in self.federations.items():
            if cid in config['chats']:
                fed = federation
                break

        async def check_admin(user_id):
            try:
                return (await self.client.get_permissions(cid, user_id)).is_admin
            except ValueError:
                return (user_id in loader.dispatcher.security._owner or user_id in loader.dispatcher.security._sudo)

        async def check_member(user_id):
            try:
                await self.client.get_permissions(cid, user_id)
                return True
            except Exception:
                return False

        if not fed:
            if str(cid) not in self.warns:
                return await utils.answer(message, self.strings('chat_not_in_db', message))

            async def send_user_warns(usid):
                if str(cid) not in self.warns:
                    await utils.answer(message, self.strings('chat_not_in_db', message))
                    return
                elif usid not in self.warns[str(cid)]['w'] or len(self.warns[str(cid)]['w'][usid]) == 0:
                    user_obj = await self.client.get_entity(usid)
                    await utils.answer(message, self.strings('no_warns', message).format(user_obj.id,
                                                                                         user_obj.first_name if getattr(
                                                                                             user_obj, 'first_name',
                                                                                             None) is not None else user_obj.title))
                else:
                    user_obj = await self.client.get_entity(usid)
                    await utils.answer(message, self.strings('warns', message).format(user_obj.id,
                                                                                      user_obj.first_name if getattr(
                                                                                          user_obj,
                                                                                          'first_name',
                                                                                          None) is not None else user_obj.title,
                                                                                      len(self.warns[str(cid)]['w'][usid]),
                                                                                      self.warns[str(cid)]['l'],
                                                                                      '\n    🏴󠁧󠁢󠁥󠁮󠁧󠁿 '.join(
                                                                                          self.warns[str(cid)]['w'][usid])))

            if not await check_admin(message.sender_id):
                await send_user_warns(message.sender_id)
            else:
                reply = await message.get_reply_message()
                args = utils.get_args_raw(message)
                if not reply and not args:
                    res = self.strings('warns_adm', message)
                    for user, warns in self.warns[str(cid)]['w'].copy().items():
                        try:
                            user_obj = await self.client.get_entity(int(user))
                        except Exception:
                            del self.warns[str(cid)]['w'][user]
                            continue

                        if not await check_member(int(user)):
                            del self.warns[str(cid)]['w'][user]
                            continue

                        if isinstance(user_obj, telethon.tl.types.User):
                            try:
                                name = user_obj.first_name + ' ' + (user_obj.last_name if getattr(user_obj, 'last_name', '') is not None else '')
                            except TypeError:
                                del self.warns[str(cid)]['w'][user]
                                continue
                        else:
                            name = user_obj.title

                        res += "🐺 <b><a href=\"tg://user?id=" + str(user_obj.id) + "\">" + name + '</a></b>\n'
                        for warn in warns:
                            res += "<code>   </code>🏴󠁧󠁢󠁥󠁮󠁧󠁿 <i>" + warn + '</i>\n'

                    await utils.answer(message, res)
                    return
                elif reply:
                    await send_user_warns(reply.sender_id)
                elif args:
                    await send_user_warns(args)
        else:
            if not self.federations[fed]['warns']:
                return await utils.answer(message, self.strings('no_fed_warns', message))


            async def send_user_warns(usid):
                if not self.federations[fed]['warns']:
                    await utils.answer(message, self.strings('no_fed_warns', message))
                    return

                elif str(usid) not in self.federations[fed]['warns'] or len(self.federations[fed]['warns'][str(usid)]) == 0:
                    user_obj = await self.client.get_entity(usid)
                    await utils.answer(message, self.strings('no_warns', message).format(user_obj.id,
                                                                                         user_obj.first_name if getattr(
                                                                                             user_obj, 'first_name',
                                                                                             None) is not None else user_obj.title))
                else:
                    user_obj = await self.client.get_entity(usid)
                    await utils.answer(message, self.strings('warns', message).format(user_obj.id,
                                                                                      user_obj.first_name if getattr(
                                                                                          user_obj,
                                                                                          'first_name',
                                                                                          None) is not None else user_obj.title,
                                                                                      len(self.federations[fed]['warns'][str(usid)]),
                                                                                      7,
                                                                                      '\n    🏴󠁧󠁢󠁥󠁮󠁧󠁿 '.join(
                                                                                          self.federations[fed]['warns'][str(usid)])))

            if not await check_admin(message.sender_id):
                await send_user_warns(message.sender_id)
            else:
                reply = await message.get_reply_message()
                args = utils.get_args_raw(message)
                if not reply and not args:
                    res = self.strings('warns_adm_fed', message)
                    for user, warns in self.federations[fed]['warns'].copy().items():
                        try:
                            user_obj = await self.client.get_entity(int(user))
                        except Exception:
                            del self.federations[fed]['warns'][user]
                            continue

                        if isinstance(user_obj, telethon.tl.types.User):
                            try:
                                name = user_obj.first_name + ' ' + (user_obj.last_name if getattr(user_obj, 'last_name', '') is not None else '')
                            except TypeError:
                                del self.federations[fed]['warns'][user]
                                continue
                        else:
                            name = user_obj.title

                        res += "🐺 <b><a href=\"tg://user?id=" + str(user_obj.id) + "\">" + name + '</a></b>\n'
                        for warn in warns:
                            res += "<code>   </code>🏴󠁧󠁢󠁥󠁮󠁧󠁿 <i>" + warn + '</i>\n'

                    await utils.answer(message, res)
                    return
                elif reply:
                    await send_user_warns(reply.sender_id)
                elif args:
                    await send_user_warns(args)


    @loader.group_admin_ban_users
    async def dwarncmd(self, message):
        """<ответить | айди | username> - Удалить последнее предупреждение"""
        if message.is_private:
            await message.delete()
            return

        cid = str(utils.get_chat_id(message))
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user = None

        if reply:
            user = await self.client.get_entity(reply.sender_id)
        else:
            try:
                args = int(args)
            except Exception:
                pass

            try:
                user = await self.client.get_entity(args)
            except IndexError:
                return await utils.answer(message, self.strings('args', message))

        fed = None
        for federation, config in self.federations.items():
            if int(cid) in config['chats']:
                fed = federation
                break

        if not fed:
            if cid not in self.warns:
                return await utils.answer(message, self.strings('chat_not_in_db', message))

            if str(user.id) not in self.warns[cid]['w']:
                return await utils.answer(message, self.strings('no_warns').format(user.id,
                                                                user.first_name if getattr(user, 'first_name',
                                                                                           None) is not None else user.title))

            del self.warns[cid]['w'][str(user.id)][-1]
            await utils.answer(message, self.strings('dwarn', message).format(user.id,
                                                                              user.first_name if getattr(user, 'first_name',
                                                                                                         None) is not None else user.title))
            self.db.set('InnoChats', 'warns', self.warns)
        else:
            if not self.federations[fed]['warns']:
                return await utils.answer(message, self.strings('no_fed_warns', message))

            if str(user.id) not in self.federations[fed]['warns']:
                return await utils.answer(message, self.strings('no_warns').format(user.id,
                                                                user.first_name if getattr(user, 'first_name',
                                                                                           None) is not None else user.title))

            del self.federations[fed]['warns'][str(user.id)][-1]
            await utils.answer(message, self.strings('dwarn_fed', message).format(user.id,
                                                                              user.first_name if getattr(user, 'first_name',
                                                                                                         None) is not None else user.title))
            self.db.set('InnoChats', 'federations', self.federations)

    @loader.group_admin_ban_users
    async def clrwarnscmd(self, message):
        """<ответить | айди | username> - Удалить все предупреждения от пользователя
"""
        if message.is_private:
            await message.delete()
            return

        cid = str(utils.get_chat_id(message))
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self.client.get_entity(reply.sender_id)
        else:
            try:
                args = int(args)
            except Exception:
                pass

            try:
                user = await self.client.get_entity(args)
            except IndexError:
                return await utils.answer(message, self.strings('args', message))

        fed = None
        for federation, config in self.federations.items():
            if int(cid) in config['chats']:
                fed = federation
                break

        if not fed:
            if cid not in self.warns:
                return await utils.answer(message, self.strings('chat_not_in_db', message))

            if str(user.id) not in self.warns[cid]['w']:
                return await utils.answer(message, self.strings('no_warns').format(user.id, user.first_name if getattr(user,
                                                                                                                       'first_name',
                                                                                                                       None) is not None else user.title))

            del self.warns[cid]['w'][str(user.id)]
            await utils.answer(message, self.strings('clrwarns', message).format(user.id, user.first_name if getattr(user,
                                                                                                                     'first_name',
                                                                                                                     None) is not None else user.title))
            self.db.set('InnoChats', 'warns', self.warns)
        else:
            if not self.federations[fed]['warns']:
                return await utils.answer(message, self.strings('no_fed_warns', message))

            if str(user.id) not in self.federations[fed]['warns']:
                return await utils.answer(message, self.strings('no_warns').format(user.id, user.first_name if getattr(user,
                                                                                                                       'first_name',
                                                                                                                       None) is not None else user.title))

            del self.federations[fed]['warns'][str(user.id)]
            await utils.answer(message, self.strings('clrwarns_fed', message).format(user.id, user.first_name if getattr(user,
                                                                                                                     'first_name',
                                                                                                                     None) is not None else user.title))
            self.db.set('InnoChats', 'federations', self.federations)

    @loader.group_admin_ban_users
    async def warnsactioncmd(self, message):
        """<отключить звук | бан | кик> - Установить действие при достижении лимита"""
        if message.is_private:
            await message.delete()
            return

        args = utils.get_args_raw(message)
        if not args or args not in ['mute', 'kick', 'ban']:
            return await utils.answer(message, self.strings('args', message))

        cid = utils.get_chat_id(message)

        if str(cid) not in self.warns:
            self.warns[str(cid)] = {
                'a': 'mute',
                'l': 5,
                'w': {}
            }

        self.warns[str(cid)]['a'] = args
        await utils.answer(message, self.strings('new_a', message).format(args))

    @loader.group_admin_ban_users
    async def warnslimitcmd(self, message):
        """<limit:int> - Установить лимит предупреждений"""
        if message.is_private:
            await message.delete()
            return

        args = utils.get_args_raw(message)
        try:
            args = int(args)
        except Exception:
            return await utils.answer(message, self.strings('args', message))

        cid = utils.get_chat_id(message)

        if str(cid) not in self.warns:
            self.warns[str(cid)] = {
                'a': 'mute',
                'l': 5,
                'w': {}
            }

        self.warns[str(cid)]['l'] = args
        await utils.answer(message, self.strings('new_l').format(args))

    @loader.group_owner
    async def welcomecmd(self, message):
        """<текст> - Изменить текст приветствия"""
        cid = str(utils.get_chat_id(message))
        args = utils.get_args_raw(message)
        if cid not in self.chats:
            self.chats[cid] = {}

        if args:
            self.chats[cid]['welcome'] = args
            await utils.answer(message, self.strings('welcome'))
        else:
            if 'welcome' in self.chats[cid]:
                del self.chats[cid]['welcome']

            await utils.answer(message, self.strings('unwelcome'))

        self.db.set('InnoChats', 'chats', self.chats)


    @loader.group_owner
    async def antichannelcmd(self, message):
        """Переключить удаление сообщений из каналов"""
        cid = str(utils.get_chat_id(message))
        if cid not in self.chats:
            self.chats[cid] = {}

        if 'antichannel' not in self.chats[cid]:
            self.chats[cid]['antichannel'] = True
            await utils.answer(message, self.strings('antichannel').format('on'))
        else:
            del self.chats[cid]['antichannel']
            await utils.answer(message, self.strings('antichannel').format('off'))

        self.db.set('InnoChats', 'chats', self.chats)


    @loader.group_owner
    async def antifloodcmd(self, message):
        """Переключить Антифлуд"""
        chat = str(utils.get_chat_id(message))
        if chat not in self.chats:
            self.chats[chat] = {}

        args = utils.get_args_raw(message)

        if args not in ['warn', 'ban', 'kick', 'mute', 'delmsg']:
            if 'antiflood' in self.chats[chat]:
                del self.chats[chat]['antiflood']
            await utils.answer(message, self.strings('antiflood').format('off', 'none'))
        else:
            self.chats[chat]['antiflood'] = args
            await utils.answer(message, self.strings('antiflood').format('on', args))

        self.db.set('InnoChats', 'chats', self.chats)



    @loader.group_owner
    async def antispoilercmd(self, message):
        """Переключить сообщения с удалением спойлера"""
        cid = str(utils.get_chat_id(message))
        if cid not in self.chats:
            self.chats[cid] = {}

        if 'antispoiler' not in self.chats[cid]:
            self.chats[cid]['antispoiler'] = True
            await utils.answer(message, self.strings('antispoiler').format('on'))
        else:
            del self.chats[cid]['antispoiler']
            await utils.answer(message, self.strings('antispoiler').format('off'))

        self.db.set('InnoChats', 'chats', self.chats)

    @loader.group_owner
    async def defcmd(self, message):
        """<пользователь | answer> - Переключить неуязвимость пользователя"""
        if message.is_private:
            await message.delete()
            return

        cid = str(utils.get_chat_id(message))
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self.client.get_entity(reply.sender_id)
        else:
            try:
                args = int(args)
            except Exception:
                pass

            try:
                user = await self.client.get_entity(args)
            except IndexError:
                return await utils.answer(message, self.strings('args', message))

        if cid not in self.chats:
            self.chats[cid] = {}

        if 'defense' not in self.chats[cid]:
            self.chats[cid]['defense'] = []

        if user.id not in self.chats[cid]['defense']:
            self.chats[cid]['defense'].append(user.id)
            await utils.answer(message,
                               self.strings('defense', message).format(user.id, user.first_name if getattr(user,
                                                                                                           'first_name',
                                                                                                           None) is not None else user.title if getattr(
                                   user, 'first_name', None) is not None else user.title, 'on'))
        else:
            self.chats[cid]['defense'].remove(user.id)
            await utils.answer(message,
                               self.strings('defense', message).format(user.id, user.first_name if getattr(user,
                                                                                                           'first_name',
                                                                                                           None) is not None else user.title if getattr(
                                   user, 'first_name', None) is not None else user.title, 'off'))

        self.db.set('InnoChats', 'chats', self.chats)

    @loader.group_owner
    async def gdefcmd(self, message):
        """<пользователь | ответ> - Переключить глобальную неуязвимость пользователя"""
        if message.is_private:
            await message.delete()
            return

        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self.client.get_entity(reply.sender_id)
        else:
            try:
                args = int(args)
            except Exception:
                pass

            try:
                user = await self.client.get_entity(args)
            except IndexError:
                return await utils.answer(message, self.strings('args', message))

        if user.id not in self.db.get('InnoChats', 'gdefense', []):
            self.db.set('InnoChats', 'gdefense', self.db.get('InnoChats', 'gdefense', []) + [user.id])
            await utils.answer(message,
                               self.strings('defense', message).format(user.id, user.first_name if getattr(user,
                                                                                                           'first_name',
                                                                                                           None) is not None else user.title if getattr(
                                   user, 'first_name', None) is not None else user.title, 'on'))
        else:
            self.db.set('InnoChats', 'gdefense', list(set(self.db.get('InnoChats', 'gdefense', [])) - set([user.id])))
            await utils.answer(message,
                               self.strings('defense', message).format(user.id, user.first_name if getattr(user,
                                                                                                           'first_name',
                                                                                                           None) is not None else user.title if getattr(
                                   user, 'first_name', None) is not None else user.title, 'off'))

        self.db.set('InnoChats', 'chats', self.chats)

    @loader.group_owner
    async def deflistcmd(self, message):
        """Показать неуязвимых пользователей"""
        chat = str(utils.get_chat_id(message))
        if chat not in self.chats or not self.chats[chat] or 'defense' not in self.chats[chat] or not self.chats[chat][
            'defense']:
            return await utils.answer(message, self.strings('no_defense', message))

        res = ""
        defense = self.chats[chat]['defense']
        for user in defense.copy():
            try:
                u = await self.client.get_entity(user)
            except Exception:
                self.chats[chat]['defense'].remove(user)
                continue

            tit = u.first_name if getattr(u, 'first_name', None) is not None else u.title
            res += f"  🇻🇦 <a href=\"tg://user?id={u.id}\">{tit}{(' ' + u.last_name) if getattr(u, 'last_name', None) is not None else ''}</a>\n"

        return await utils.answer(message, self.strings('defense_list').format(res))

    @loader.group_owner
    async def gdeflistcmd(self, message):
        """Показать глобальных неуязвимых пользователей"""
        if not self.db.get('InnoChats', 'gdefense', []):
            return await utils.answer(message, self.strings('no_defense', message))

        res = ""
        defense = self.db.get('InnoChats', 'gdefense', [])
        for user in defense.copy():
            try:
                u = await self.client.get_entity(user)
            except Exception:
                self.db.set('InnoChats', 'gdefense', list(set(self.db.get('InnoChats', 'gdefense', [])) - set([user])))
                continue

            tit = u.first_name if getattr(u, 'first_name', None) is not None else u.title
            res += f"  🇻🇦 <a href=\"tg://user?id={u.id}\">{tit}{(' ' + u.last_name) if getattr(u, 'last_name', None) is not None else ''}</a>\n"

        return await utils.answer(message, self.strings('defense_list').replace('in current chat', '').format(res))


    async def antinsfwcmd(self, message):
        """Переключить защиту от nsfw в текущем чате"""
        if message.is_private:
            await message.delete()
            return

        chat = str(utils.get_chat_id(message))
        if chat not in self.chats:
            self.chats[chat] = {}

        if not self.token:
            async with self.client.conversation('@innoapi_auth_' + 'bot') as conv:
                m = await conv.send_message("@get+innochat+token")
                res = await conv.get_response()
                await conv.mark_read()
                self.token = res.raw_text
                await m.delete()
                await res.delete()
                self.db.set('InnoChats', 'apitoken', self.token)


        if 'antinsfw' in self.chats[chat]:
            del self.chats[chat]['antinsfw']
            await utils.answer(message, self.strings('nsfw_toggle').format('off'))
        else:
            self.chats[chat]['antinsfw'] = True
            await utils.answer(message, self.strings('nsfw_toggle').format('on'))

        self.db.set('InnoChats', 'chats', self.chats)


    async def watcher(self, message):

        try:
            cid = str(utils.get_chat_id(message))

            if cid not in self.chats or not self.chats[cid]:
                return

            user = message.sender_id if getattr(message, 'from_id', None) is not None else 0
            if user < 0:
                user = int(str(user)[4:])
            # logger.info(user)
            if 'defense' in self.chats[cid] and user in self.chats[cid]['defense']:
                return

            if user in self.db.get('InnoChats', 'gdefense', []):
                return

            try:
                if (await self.client.get_permissions(int(cid), message.sender_id)).is_admin: return
            except Exception:
                pass

            # Anti Raid:

            if 'antiraid' in self.chats[cid]:
                if getattr(message, "user_joined", False) or getattr(message, "user_added", False):
                    user = await message.get_user()
                    chat = await message.get_chat()
                    user_name = getattr(user, 'first_name', '') + ' ' + (
                        user.last_name if getattr(user, 'last_name', '') is not None else '')
                    action = self.chats[cid]['antiraid']
                    if action == "kick":
                        await self.client.send_message('me', self.strings('antiraid').format('kicked', user, user_name,
                                                                                             chat.title))
                        await self.client.kick_participant(int(cid), user)
                    elif action == "ban":
                        await self.client.send_message('me', self.strings('antiraid').format('banned', user, user_name,
                                                                                             chat.title))
                        await self.client(telethon.tl.functions.channels.EditBannedRequest(int(cid), user,
                                                                                           telethon.tl.types.ChatBannedRights(
                                                                                               until_date=0,
                                                                                               view_messages=True,
                                                                                               send_messages=True,
                                                                                               send_media=True,
                                                                                               send_stickers=True,
                                                                                               send_gifs=True,
                                                                                               send_games=True,
                                                                                               send_inline=True,
                                                                                               embed_links=True)))
                    elif action == "mute":
                        await self.client.send_message('me', self.strings('antiraid').format('muted', user, user_name,
                                                                                             chat.title))
                        await self.client(telethon.tl.functions.channels.EditBannedRequest(int(cid), user,
                                                                                           telethon.tl.types.ChatBannedRights(
                                                                                               until_date=0,
                                                                                               send_messages=True)))

                    return

            if 'antisex' in self.chats[cid]:
                if getattr(message, "user_joined", False) or getattr(message, "user_added", False):
                    user = await message.get_user()
                    chat = await message.get_chat()
                    user_name = getattr(user, 'first_name', '') + ' ' + (
                        user.last_name if getattr(user, 'last_name', '') is not None else '')
                    replacing = {
                        "3Z8z": "З",
                        "HN7hn": "Н",
                        "A5a": "А",
                        "K4k": "К",
                        "O0o": "О",
                        "Mm": "М",
                        "CSc": "С"
                    }

                    for key, value in replacing.items():
                        for letter in list(key):
                            user_name = user_name.replace(letter, value)

                    # logger.info(user_name)

                    if 'ЗНАКОМС' in user_name:
                        # user_name = ''.join([_ for _ in user_name if _ in string.hexdigits])
                        action = self.chats[cid]['antisex']
                        if action == "kick":
                            await self.client.send_message(chat,
                                                           self.strings('antisex').format(user.id, user_name, 'kicked'))
                            await self.client.kick_participant(int(cid), user)
                        elif action == "ban":
                            await self.client.send_message(chat,
                                                           self.strings('antisex').format(user.id, user_name, 'banned'))
                            await self.client(telethon.tl.functions.channels.EditBannedRequest(int(cid), user,
                                                                                               telethon.tl.types.ChatBannedRights(
                                                                                                   until_date=0,
                                                                                                   view_messages=True,
                                                                                                   send_messages=True,
                                                                                                   send_media=True,
                                                                                                   send_stickers=True,
                                                                                                   send_gifs=True,
                                                                                                   send_games=True,
                                                                                                   send_inline=True,
                                                                                                   embed_links=True)))
                        elif action == "mute":
                            await self.client.send_message(chat,
                                                           self.strings('antisex').format(user.id, user_name, 'muted'))
                            await self.client(telethon.tl.functions.channels.EditBannedRequest(int(cid), user,
                                                                                               telethon.tl.types.ChatBannedRights(
                                                                                                   until_date=0,
                                                                                                   send_messages=True)))

                        return

            if 'welcome' in self.chats[cid]:
                if getattr(message, "user_joined", False) or getattr(message, "user_added", False):
                    user = await message.get_user()
                    chat = await message.get_chat()
                    await self.client.send_message(int(cid), self.chats[cid]['welcome'].replace('{user}',
                                                                                                user.first_name if getattr(
                                                                                                    user, 'first_name',
                                                                                                    None) is not None else user.title).replace(
                        '{chat}', chat.title).replace('{mention}', '<a href="tg://user?id=' + str(
                        user.id) + '">' + user.first_name if getattr(user, 'first_name',
                                                                     None) is not None else user.title + '</a>'),
                                                   reply_to=message.action_message.id)

                    return

            user = message.sender_id or None

            # AntiChannel:

            if 'antichannel' in self.chats[cid]:
                if user < 0:
                    await message.delete()
                    return

            violation = None

            # AntiSpoiler:

            if 'antispoiler' in self.chats[cid]:
                if isinstance(message.entities, list) and [True for _ in message.entities if isinstance(_, telethon.tl.types.MessageEntitySpoiler)]:
                    await message.delete()
                    # logger.info('Spoiler!')
                    return

            # AntiFlood:
            if 'antiflood' in self.chats[cid]:
                if cid not in self.flood_cache:
                    self.flood_cache[cid] = {}

                if user not in self.flood_cache[cid]:
                    self.flood_cache[cid][user] = []

                for item in self.flood_cache[cid][user].copy():
                    if time.time() - item > self.flood_timeout:
                        self.flood_cache[cid][user].remove(item)

                self.flood_cache[cid][user].append(round(time.time(), 2))
                self.save_flood_cache()

                if len(self.flood_cache[cid][user]) >= self.flood_threshold:
                    del self.flood_cache[cid][user]
                    violation = 'flood'
                    action = self.chats[cid]['antiflood']

            # AntiNSFW:

            if 'antinsfw' in self.chats[cid]:
                if message.media is not None and isinstance(message.media, telethon.tl.types.MessageMediaPhoto):
                    photo = io.BytesIO()
                    await self.client.download_media(message.media, photo)
                    photo.seek(0)
                    
                    response = requests.post('https://api.innocoffee.ru/check_nsfw', files={'file': photo}, headers={
                        'Authorization': f'Bearer {self.token}'
                    }).json()

                    # await utils.answer(message, "<code>" + json.dumps(response, indent=4) + "</code>")

                    if response['verdict'] == 'nsfw':
                        await message.delete()
                        violation = 'nsfw_content'
                        action = 'mute'

                    # await utils.answer(message, response.text)


            # AntiLogSpam:

            if 'als' in self.chats[cid]:
                if user is not None and str(user) != self.me:
                    msid = message.id
                    self.cache[cid + "_" + str(msid)] = (user,
                                                         round(time.time()) - self.correction)
                    for key, info in self.cache.copy().items():
                        if time.time() - info[1] - self.correction >= 86400:
                            del self.cache[key]
                    self.save_cache()

            user_obj = await self.client.get_entity(int(user))
            user_name = getattr(user_obj, 'first_name', '') + ' ' + (
                user_obj.last_name if getattr(user_obj, 'last_name', '') is not None else '')

            # AntiTagAll:

            if 'antitagall' in self.chats[cid]:
                if message.text.count('tg://user?id=') >= 5:
                    violation = 'tagall'
                    action = self.chats[cid]['antitagall']

            # AntiHelp:
            if 'antihelp' in self.chats[cid]:
                search = message.text
                if '@' in search:
                    search = search[:search.find('@')]
                    tagged = True
                else:
                    tagged = False

                blocked_commands = ['help', 'dlmod', 'loadmod', 'lm', 'ping']

                if len(search.split()) > 0 and search.split()[0][1:] in blocked_commands:
                    await message.delete()


            # Arab Shield:
            if 'arabshield' in self.chats[cid]:
                to_check = getattr(message, 'message', '') + \
                           getattr(message, 'caption', '') + user_name
                if len(re.findall('[\u4e00-\u9fff]+', to_check)) != 0 or len(
                        re.findall('[\u0621-\u064A]+', to_check)) != 0:
                    violation = 'arabic_nickname'
                    action = self.chats[cid]['arabshield']

            if violation is None:
                return

            await self.punish(int(cid), int(user), violation, action, user_name)

            try:
                await message.delete()
            except Exception:
                pass

        except Exception as e:
            logger.exception(e)