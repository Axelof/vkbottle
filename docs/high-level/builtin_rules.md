# Все встроенные правила

---

## PeerRule

`PeerRule(from_chat: bool = True)`

Нужно для ограничения источника сообщения, `PeerRule(from_chat=False)` например, будет указывать на то, что сообщение должно быть из личного диалога с ботом.

---

## MentionRule

`MentionRule(mention_only: bool = False)`

Используется для проверки на то, что бот был упомянут в сообщении. Параметр `mention_only` используется чтобы указать, что кроме упоминания в сообщении быть ничего не должно, в ином случае из сообщения удаляется упоминание чтобы другие правила могли обработать уже сам текст.

---

## CommandRule

```python
CommandRule(
    command_text,
    prefixes,
    args_count = 0,
    sep = " "
)
```

Используется для того чтобы реагировать на команды

Команда выглядит так:

```
{prefix}{command_text}{sep.join(args)}
```

В `command_text` можно передать несколько вариантов названия команды.

В `prefixes` можно передать несколько возможных префиксов (например: '/', '!').

В `args_count` передается количество обязательных аргументов с `sep` в качестве разделителя

---

## VBMLRule

```python
VBMLRule(
    pattern,
    patcher = None,
    flags = None
)
```

Используется в качестве парсера текстов сообщений. Разметка vbml исторически была сделана специально для фреймворка, чтобы легко писать паттерны с валидируемыми аргументами.

Пример:

```python
rule = VBMLRule("/cmd <eggs:int>")
rst = await rule.check(Message(text="/cmd 11", ...))
assert rst == {"eggs": 11}
```

Больше документации [CLICK 🤩](https://github.com/tesseradecade/vbml/blob/master/docs/index.md)

---

## RegexRule

`RegexRule(regexp)`

Используется для проверки на соответствие текста сообщения регулярному выражению.

---

## StickerRule

`StickerRule(sticker_ids = None)`

Используется для того чтобы отлавливать отправку стикеров в сообщении. Если sticker_ids = None, то проходить будет любое сообщение содержащее стикер.

---

## FromPeerRule

`FromPeerRule(peer_ids)`

Используется для отлова сообщений отправленных пользователем/группой с одним из указанных ID.

---

## AttachementTypeRule

`AttachementTypeRule(attachment_types)`

Используется для отлова сообщений с указанным типом вложений (например: `photo`)


---

## ForwardMessagesRule

Используется для того, чтобы проверить, что сообщение содержит в себе вложенные сообщения.

---

## ReplyMessageRule

`ReplyMessageRule(reply_message: bool = True)`

--

## GeoRule

Используется для того чтобы отлавливать сообщения с геометкой.

**WIP ...**
