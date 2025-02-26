### Назначение системы

В настольных играх иногда, чтобы продолжить игру, нужно всего-лишь уточнить пункт правил, но:
Правила не всегда есть под рукой
Иногда для поиска нужного пункта приходится тратить время, за которое можно было бы совершить целое множество ходов
Сложность поиска приводит к нежеланию им заниматься и зачастую игра продолжается по правилам, которые остались в памяти у одного из участников.

Консультант по правилам настольных игр поможет ответить на интересующий вопрос и укажет нужный пункт правил, будучи всегда под рукой.


### Портрет пользователя

- Любитель настольных игр.

Егор Леонидов, 20 лет.
Место проживания: Москва.
Семейное положение: не женат.
Сфера занятости и уровень зарплаты: студент, -300к/нс.
Должность: студент.
Связанные с ней проблемы: отсутствие сна, плотный график, огромный объём информации.
Потребности, желания, фобии: Для быстрого ответа на вопросы по настольным играм, Егору особенно удобно будет использовать мессенджер телеграм. Готов использовать систему, если в ней будет просто разобраться и не нужно будет за неё платить.

- Администратор особого клуба настольных игр.

То же, что и любитель настольных игр.

### User stories:

1. Как пользователь, я хочу уточнять правила настольных игр, чтобы не тратить много времени на поиск информации самому.

- Ответ на запрос пользователя, содержащий запрашиваемую им информацию, сгенерированный RAG.
- Если системе не хватает информации для точного ответа, она должна попросить пользователя уточнить вопрос.
- Если система перегружена и не может обработать запрос пользователя в ближайшее время, она должна поставить запрос в очередь и написать об этом.
- Если запрос состоит из нескольких вопросов, система должна ответить на них все.

2. Как пользователь, я хочу иметь возможность выбора правил своей игры, чтобы получать точные ответы именно по конкретной игре.

- Выбор пользователем нужной настольной игры при начале сценария общения.
- Сбрасывание выбора при завершении диалога или неактивности в течении часа.

3. Как пользователь, я хочу иметь возможность самому уточнить пункт правил, чтобы быть уверенным в ответе.

- В каждом конкретном ответе, система должна вставлять конкретный пункт правил, из которого была взята информация без модификации.
- Если пункт правил слишком большой, система должна давать ссылки на пункты правил.
- Если ответ составлен из нескольких пункт правил, система должна упомянуть их все.

4. Как пользователь, я хочу иметь возможность пересылать ответы бота в мессенджере Telegram, чтобы друзья могли ознакомиться с полным ответом одновременно со мной.

- Отправка ответов в виде сообщений Telegram.

5. Как администратор, я хочу иметь возможность добавлять, изменять и удалять правила для игр, чтобы система оставалась актуальной.

- Добавление новых правил игры и обновление осведомлённости RAG.
- Удаление старых правил игры и обновление осведомлённости RAG.
- Модификация правил игры и обновление осведомлённости RAG.

6. Как администратор, я хочу просматривать диалоги пользователей с системой, чтобы следить за качеством её работы.

- Сохранение диалогов с пользователями в базе данных.

7. Как администратор, я хочу, чтобы система сама оценивала качество своих ответов, чтобы была возможность быстро находить неудовлетворительные ответы и эффективно дорабатывать систему в слабых местах.

- При завершении диалога, система должна просить оценить её ответ по 5-бальной шкале.
- Если пользователь не отвечает, не устанавливать оценку.
- Добавление оценки в базу данных диалогов.

8. Как администратор особого клуба настольных игр, я хочу подстроить стилистику ответов системы, чтобы система подходила под наш клуб.

- Редактирование части промпта, касательно стилистики ответов.

9. Как администратор особого клуба настольных игр, я хочу развернуть сервис на своём сервере, чтобы наш клуб чувствовал себя в безопасности.

- Развёртывание через docker на localhost.
- Чтение необходимой информации из файла конфигурации.

10. Как пользователь, я хочу, чтобы система учитывала контекст диалога, чтобы мне не пришлось каждый раз заново выбирать игру.

- Фиксирование диалогов с пользователями.
- Считать диалог завершённым по истечении часа.
- Отправление извещения пользователю при завершении диалога.
