import pandas as pd

main_file_name = input('Введите название файла с которого брать основные строки (без .csv): ')
second_file_name = input('Введите название файла с которого брать 1 колонку (без .csv): ')
name_column = input('Введите название колонки которую необходимо перенести: ')


# Функция для обновления столбца в основном файле по данным из второго файла
def update_column(chunk):
    main_chunk = chunk['main']
    b_chunk = chunk['second']

    if len(main_chunk) < len(b_chunk):
        multiplier = len(b_chunk) // 12 + 1
        additional_rows = pd.concat([main_chunk.tail(12)] * multiplier, ignore_index=True)
        main_chunk = pd.concat([main_chunk, additional_rows.head(len(b_chunk) - len(main_chunk))], ignore_index=True)

    main_chunk[name_column] = b_chunk[:len(main_chunk)].values

    return main_chunk

chunksize = 100000000  # Размер блока данных для обработки

# Чтение файла с данными, которые нужно обновить (основной файл)
main_file_chunks = pd.read_csv(f'{main_file_name}.csv', chunksize=chunksize, sep=':')
# Чтение файла с данными для заполнения столбца
b_file_chunks = pd.read_csv(f'{second_file_name}.csv', chunksize=chunksize, sep=':')

# Итерация по блокам данных и обновление столбца с возможностью дублирования
updated_chunks = []
for main_chunk, b_chunk in zip(main_file_chunks, b_file_chunks):
    updated_chunk = update_column({'main': main_chunk, 'second': b_chunk})
    updated_chunks.append(updated_chunk)

# Запись обновленных данных в новый файл
updated_data = pd.concat(updated_chunks, ignore_index=True)
updated_data.to_csv('output.csv', index=False, sep=':')

print('Результат сохранен в файл output.csv')
print('Нажмите ENTER для закрытия окна...')
input()