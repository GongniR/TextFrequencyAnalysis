import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from collections import Counter


# класс для описания слова
class Word:
    def __init__(self, name_word: str, count: int, rang_dict: dict, words_count: int):
        self.name_word = name_word
        self.rang = self.__get_rang(count, rang_dict)
        self.count = count
        self.count_normal = self.__get_normal(count, words_count)
        self.count_revers = self.__get_revers(self.rang)

    def __get_rang(self, count: int, rang: dict) -> int:
        """ Получить ранг """
        return rang.get(count)

    def __get_normal(self, count: int, count_word: int) -> float:
        """Процент содержания в тексте"""
        return round(count / count_word, 4)

    def __get_revers(self, rang: int) -> float:
        """ Обратное содержание"""
        return round(0.1 * (rang ** (-1)), 3)


# Класс для графиков
class Graph:
    def __init__(self, words: Word, path: str):
        self.fig_absolute = self.__draw_absolute_graph(path, words)
        self.fig_relative = self.__draw_relative_graph(path, words)
        self.fig_revers = self.__draw_revers_graph(path, words)
        self.fig_approximation = self.__draw_approximation_graph(path, words)

    def view_graph(self) -> None:
        plt.show()

    def __bar_graph(self, x_axis: list, y_axis: list, path_save: str, aprox=False) -> plt.figure:
        x_axis = x_axis[:50]
        y_axis = y_axis[:50]
        x = np.arange(0, len(x_axis), 1)
        fig, ax = plt.subplots(figsize=(20, 12))
        ax.set_xticklabels(x_axis, rotation=90, fontsize=7)
        ax.bar(x_axis, y_axis)
        if aprox:
            x = np.arange(0, len(x_axis), 1)
            [a, b, c], res1 = curve_fit(lambda x, a, b, c: a * np.exp(-b * x) + c, x, y_axis)
            y1 = a * np.exp(-b * x) + c
            ax.plot(x, y1, 'r')
            ax.text(40, 8, f"{round(a, 4)}*exp({round(b, 4)}*x) +{round(c, 4)}", color="red")
        ax.figure.savefig(path_save)
        return ax

    def __draw_absolute_graph(self, path: str, words: Word) -> plt.figure:
        x = [word.name_word for word in words]
        y = [word.count for word in words]
        fig = self.__bar_graph(x, y, path + "absolute_words.png")
        return fig

    def __draw_relative_graph(self, path: str, words: Word) -> plt.figure:
        x = [word.name_word for word in words]
        y = [word.count_normal for word in words]
        fig = self.__bar_graph(x, y, path + "relative_words.png")
        return fig

    def __draw_revers_graph(self, path: str, words: Word) -> plt.figure:
        x = [word.name_word for word in words]
        y = [word.count_revers for word in words]
        fig = self.__bar_graph(x, y, path + "revers_words.png")
        return fig

    def __draw_approximation_graph(self, path: str, words: Word) -> plt.figure:
        x = [word.name_word for word in words]
        y = [word.count for word in words]
        fig = self.__bar_graph(x, y, path + "approximation_words.png", aprox=True)
        return fig


def get_rang(words: dict) -> dict:
    """
    Формирование ранга слов
    :param words:
    :return:
    """
    words_value = words.values()
    words_rang = sorted(set(words_value), reverse=True)
    dict_rang = {words_rang[i]: i + 1 for i in range(len(words_rang))}
    return dict_rang


def get_csv(path: str, words: Word) -> None:
    """
    Формирование csv файла результата ЧА
    :param path:
    :param words:
    :return:
    """
    path = os.path.join(path, "result")
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "words.csv")
    with open(path, "w", newline='') as file:
        name_columns = ['№', 'Словоформа', 'Ранг', 'I', 'I норм', '0.1r-1']
        writer = csv.DictWriter(file, fieldnames=name_columns)
        writer.writeheader()
        i = 0
        for word in words:
            writer.writerow({'№': i,
                             'Словоформа': word.name_word,
                             'Ранг': word.rang,
                             'I': word.count,
                             'I норм': word.count_normal,
                             '0.1r-1': word.count_revers})
            i += 1


def get_graph(path: str, words: Word, view_check=False) -> None:
    """
    Формирование графиков
    :param path:
    :param words:
    :param view_check:
    :return:
    """
    path = os.path.join(path, "graphs")
    if not os.path.exists(path):
        os.mkdir(path)
    graphs = Graph(words, path + '/')
    if view_check:
        graphs.view_graph()


def frequency_analysis_text(path_text: str, path_save_result: str) -> None:
    """
    Выполнение частотного анализа текста
    """
    if not os.path.exists(path_save_result):
        os.mkdir(path_save_result)

    # Считываем текст из файла для анализа
    text = ""
    with open(path_text, encoding='utf-8', mode='r') as file:
        text = file.read()

    # Удаляем все знаки
    items_replace = r"?!.,:;/')(0123456789“”"
    for item in items_replace:
        text = text.replace(item, '')
    text = text.replace('"', '')
    # перевод всех слов в нижний регистр
    text = text.lower()
    # разделение текста на слова
    list_text = text.split()
    # удаление всех одиночных -
    list_text.remove('—')
    new_list = []
    for i, _word in enumerate(list_text):
        items_replace = r"?!.,:;/')(0123456789“”"
        for _char in items_replace:
            _word = _word.replace(_char, '')
            _word = _word.replace('"', '')
            _word = _word.replace('—', '')
        if _word is None or len(_word) <= 0: continue; 
        new_list.append(_word)
    list_text = new_list.copy()
    # Подсчет слов и выделение каждого слова
    dict_words = dict(Counter(list_text))
    # сортировка кол-во повторов слов
    dict_tuples = sorted(dict_words.items(), key=lambda item: item[1], reverse=True)
    dict_words = {k: v for k, v in dict_tuples}
    words_list = []

    dict_rang = get_rang(dict_words)
    for i in dict_words.items():
        new_word = Word(i[0], i[1], dict_rang, len(dict_words))
        words_list.append(new_word)

    # Сохранение результата
    get_csv(path_save_result, words_list)
    get_graph(path_save_result, words_list)
    """
    Тут можно просмотреть и сохранить 
    # get_graph("linguistics_LW_1/", words_list, True)
    """


# Точка входа в программу (Запуск анализа)
if __name__ == "__main__":
    path_save = "frequency_analysis_result/"
    path_text = "text.txt"
    frequency_analysis_text(path_text, path_save)
