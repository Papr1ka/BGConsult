CREATE TABLE IF NOT EXISTS dialogs (
    dialog_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,                  -- ID пользователя в Telegram
    user_name VARCHAR(100) NOT NULL,          -- Имя пользователя
    started_at TIMESTAMP WITH TIME ZONE       -- Время начала диалога
        DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,        -- Время завершения (NULL если активен)
    status VARCHAR(20)                        -- Например: 'active', 'closed'
);

-- Таблица 2: Сообщения в диалогах
CREATE TABLE IF NOT EXISTS messages (
    message_id BIGSERIAL PRIMARY KEY,
    dialog_id BIGINT REFERENCES dialogs(dialog_id),  -- Связь с диалогом
    text TEXT,                                       -- Текст сообщения
    is_from_user BOOLEAN,                            -- От пользователя (True) или от бота (False)
    sent_at TIMESTAMP WITH TIME ZONE                 -- Время отправки
        DEFAULT CURRENT_TIMESTAMP
);

-- Таблица 3: Оценки диалогов пользователями
CREATE TABLE IF NOT EXISTS ratings (
    rating_id BIGSERIAL PRIMARY KEY,
    dialog_id BIGINT REFERENCES dialogs(dialog_id),  -- Связь с диалогом
    score SMALLINT CHECK (score BETWEEN 1 AND 5),    -- Оценка от 1 до 5
    rated_at TIMESTAMP WITH TIME ZONE                -- Время оценки
        DEFAULT CURRENT_TIMESTAMP
);