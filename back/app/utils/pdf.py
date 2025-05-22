import hashlib
import fitz

from back.app.core.paths import BASE_DIR
from back.app.models.pdf import Document

PDF_DIRECTORY = BASE_DIR / "games"


def extract_documents_from_pdf(pdf_file):
    """
    Извлекает текст из заданного PDF файла и организует его в список экземпляров Document.

    Args:
        pdf_file (str): Путь к PDF файлу.

    Returns:
        list[Document]: Список экземпляров Document, где каждый документ представляет собой страницу в PDF.
    """
    doc = fitz.open(BASE_DIR / "games" / pdf_file)
    documents = []
    filename = pdf_file.split('/')[-1]  # Имя файла без пути
    metadata = doc.metadata
    title = metadata.get("title", filename)  # Используем заголовок из метаданных или имя файла

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        document = Document(
            link=f"{page_num + 1}",
            filename=filename,
            title=title,
            text=text.strip()
        )
        documents.append(document)

    return documents


def get_file_hash(file_path):
    """
    Вычисляет MD5 хеш файла для обнаружения изменений.

    Args:
        file_path (str): Полный путь к файлу.

    Returns:
        str: MD5 хеш файла.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()


# def documents_data_from_pdf():
#     """
#     Перебирает PDF файлы в заданном каталоге, проверяет, изменился ли их хеш, и извлекает текст
#     из обновленных файлов.
#
#     Returns:
#         list[Document]: Список извлеченных экземпляров Document, или None, если обновленных файлов нет.
#     """
#     for pdf_file in os.listdir(PDF_DIRECTORY):
#         if pdf_file.endswith('.pdf'):
#             full_path = os.path.join(PDF_DIRECTORY, pdf_file)
#             current_hash = get_file_hash(full_path)
#
#             if pdf_file not in pdf_hashes or pdf_hashes[pdf_file] != current_hash:
#                 pdf_hashes[pdf_file] = current_hash  # Обновляем хеш
#                 return extract_documents_from_pdf(full_path)
#
#     return None  # Возвращаем None, если нет обновленных файлов


def find_intervals(indexies):
    """
    Находит интервалы индексов с учетом значений на -2, -1, +1 и +2 от каждого исходного индекса.

    Для каждого индекса добавляются значения на 2 позиции влево и вправо, после чего находят
    последовательные смежные интервалы.

    :param indexies: Список исходных индексов
    :return: Список интервалов в виде пар [начало, конец]
    """
    numbers = []
    # Создание расширенного списка индексов с добавлением -2, -1, +1, +2
    for i in indexies:
        numbers += [i - 2, i - 1, i, i + 1, i + 2]

    # Удаление дубликатов и сортировка
    numbers = list(x for x in set(numbers) if x >=0)
    numbers.sort()

    intervals = []
    start = numbers[0]

    # Поиск последовательных интервалов
    for i in range(1, len(numbers)):
        # Если текущее число не является последовательным с предыдущим, завершаем интервал
        if numbers[i] != numbers[i - 1] + 1:
            intervals.append([start, numbers[i - 1]])
            start = numbers[i]

    # Добавление последнего интервала
    intervals.append([start, numbers[-1]])

    return intervals

def split_text_into_chunks(text, chunk_size=512):
    """
    Разбивает текст на чанки заданного размера без использования скользящего окна.

    Args:
        text (str): Входной текст для разбиения.
        chunk_size (int): Максимальный размер чанка в символах.

    Returns:
        list[str]: Список чанков текста.
    """
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        # Проверка, помещается ли текущее слово в текущий чанк
        if len(current_chunk) + len(word) + 1 <= chunk_size:  # +1 для пробела
            if current_chunk:  # Если текущий чанк не пустой, добавляем пробел
                current_chunk += " "
            current_chunk += word
        else:
            if current_chunk:  # Если текущий чанк не пустой, добавляем его в список чанков
                chunks.append(current_chunk)
            current_chunk = word  # Начинаем новый чанк с текущего слова

    # Добавляем последний чанк, если он не пустой
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def prepare_data_for_qdrant(documents, chunk_size=512):
    """
    Подготавливает данные для загрузки в Qdrant, разбивая текст документов на фрагменты.

    Args:
        documents (list[Document]): Список документов для подготовки данных.
        chunk_size (int): Максимальный размер чанка в символах.

    Returns:
        list[dict]: Список подготовленных данных для загрузки в Qdrant.
    """
    data = []
    for document in documents:
        chunks = split_text_into_chunks(document.text, chunk_size)
        for chunk in chunks:
            data.append({
                "text": chunk,
                "link": document.link,
                "filename": document.filename,
                "title": document.title,
            })
    return data
