import random
import pandas
import numpy
import warnings
from strgen import StringGenerator
import pkg_resources


# ===========================================================
# Load words
# ===========================================================
def load_words_data_frame():
    """Return a dataframe with words.

    Contains the following fields:
        Word          word
        KnownWordQ    is a known word True/False
        KnownWordQ    is a known word True/False
        KnownWordQ    is a known word True/False
    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    with pkg_resources.resource_stream(__name__, 'resources/dfEnglishWords.csv') as stream:
        dfRes = pandas.read_csv(stream, encoding='latin-1')
        stream.close()

    return dfRes


# ===========================================================
# Load pet names
# ===========================================================
def load_pet_names_data_frame():
    """Return a dataframe with pet names.

    Contains the following fields:
        Species       species
        Name          pet name
        Count         how many licenses with that specie-name pair
    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    with pkg_resources.resource_stream(__name__, 'resources/dfPetNameCounts.csv') as stream:
        dfData = pandas.read_csv(stream, encoding='latin-1')
        stream.close()
        wsum = sum(dfData.Count)
        dfData["Weight"] = [x / wsum for x in dfData.Count]
    return dfData


# ===========================================================
# Random words
# ===========================================================

def random_string(size=1, chars=5, pattern: str = r'[\l\d]'):
    """Generates random strings with specified size and number of characters."""

    if isinstance(chars, type(None)):
        nchars = numpy.random.poisson(lam=5, size=1)
        nchars = 1 if nchars == 0 else nchars
    elif isinstance(chars, int) and chars > 1:
        nchars = chars
    else:
        raise TypeError("The second argument is expected to be positive integer of None.")

    if isinstance(size, int) and size == 1:
        return StringGenerator(pattern + "{" + str(nchars) + "}").render()
    elif isinstance(size, int) and size > 1:
        return StringGenerator(pattern + "{" + str(nchars) + "}").render_list(size, unique=True)
    elif isinstance(size, type(None)):
        return random_string(1)
    else:
        raise TypeError("The first argument is expected to be positive integer of None.")


# ===========================================================
# Random words
# ===========================================================

# Read resources
dfWords = load_words_data_frame()


def random_word(size=1, kind=None, language="English"):
    """Generates random words with specified size and kind"""

    if not isinstance(size, int) and size > 0:
        raise TypeError("The first argument is expected to be positive integer.")

    if not isinstance(language, str) and language.lower() == 'english':
        raise TypeError("""The argument language is expected to be one of 'English' or None. 
        (Only English words are supported at this time.)""")

    if isinstance(kind, type(None)):
        mkind = "any"
    elif isinstance(kind, str):
        mkind = kind
    else:
        warnings.warn("The argument 'kind' is expected to be string or None. Continuing with 'Any'.",
                      UserWarning)
        mkind = "any"

    if mkind.lower() == "any":
        res = random.sample(list(dfWords["Word"]), k=size)
    elif mkind.lower() in "known":
        res = random.sample(list(dfWords[dfWords.KnownWordQ]["Word"]), k=size)
    elif mkind.lower() == "common":
        res = random.sample(list(dfWords[dfWords.CommonWordQ]["Word"]), k=size)
    elif mkind.lower() in {"stop", "stopword"}:
        res = random.sample(list(dfWords[dfWords.StopWordQ]["Word"]), k=size)
    else:
        warnings.warn("The argument 'kind' is expected to be one of 'Any', 'Known', 'Common', 'Stopword', or None.",
                      UserWarning)
        return random_word(size=size, kind="Any", language=language)

    if size == 1:
        return res[0]
    return res


# ===========================================================
# Random pet names
# ===========================================================

dfPetNames = load_pet_names_data_frame()


def random_pet_name(size=1, species=None, weighted=True):
    """Generates random pet names; popularity-based weighted sampling and species can be specified."""
    if not (isinstance(size, int) and size > 0):
        raise TypeError("The first argument is expected to be a positive integer.")

    allSpecies = set(["Any", "Cat", "Dog", "Goat", "Pig"])

    if not (isinstance(species, type(None)) or isinstance(species, str) and species.capitalize() in allSpecies):
        warnings.warn("The argument 'species' is expected to be one of %, or None. Continuing with Any.",
                      UserWarning)
        species = "Any"

    if weighted:
        weights = dfPetNames.Weight
    else:
        weights = None

    if isinstance(species, type(None)) or species.capitalize() == 'Any':
        res = numpy.random.choice(dfPetNames.Name, size=size, p=weights)
    else:
        dfPetNames2 = dfPetNames[dfPetNames.Species == species.capitalize()]
        names = list(dfPetNames2.Name)
        weights = list(dfPetNames2.Weight)
        sws = sum(weights)
        weights = [x / sws for x in weights]
        res = numpy.random.choice(names, size=size, p=weights)

    if size == 1:
        return res[0]
    return list(res)


# ===========================================================
# Random pet pretentious job title
# ===========================================================

pretentiousJobTitleWords = {
    'english':
        {
            'uno': ['Lead', 'Senior', 'Direct', 'Corporate', 'Dynamic',
                    'Future', 'Product', 'National', 'Regional', 'District',
                    'Central', 'Global', 'Relational', 'Customer', 'Investor',
                    'Dynamic', 'International', 'Legacy', 'Forward', 'Interactive',
                    'Internal', 'Human', 'Chief', 'Principal'],
            'zwei': ('Solutions', 'Program', 'Brand', 'Security', 'Research',
                     'Marketing', 'Directives', 'Implementation', 'Integration',
                     'Functionality', 'Response', 'Paradigm', 'Tactics', 'Identity',
                     'Markets', 'Group', 'Resonance', 'Applications', 'Optimization',
                     'Operations', 'Infrastructure', 'Intranet', 'Communications',
                     'Web', 'Branding', 'Quality', 'Assurance', 'Impact', 'Mobility',
                     'Ideation', 'Data', 'Creative', 'Configuration',
                     'Accountability', 'Interactions', 'Factors', 'Usability',
                     'Metrics', 'Team'),
            'trois': ('Supervisor', 'Associate', 'Executive', 'Liason',
                      'Officer', 'Manager', 'Engineer', 'Specialist', 'Director',
                      'Coordinator', 'Administrator', 'Architect', 'Analyst',
                      'Designer', 'Planner', 'Synergist', 'Orchestrator', 'Technician',
                      'Developer', 'Producer', 'Consultant', 'Assistant',
                      'Facilitator', 'Agent', 'Representative', 'Strategist')
        },
    'bulgarian':
        {
            'uno': ('Бъдещ', 'Водещ', 'Главен', 'Старши', 'Човешки', 'Вътрешен',
                    'Глобален', 'Директен', 'Клиентов', 'Областен', 'Динамичен',
                    'Динамичен', 'Централен', 'Инвестиращ', 'Национален', 'Регионален',
                    'Релационен', 'Наследствен', 'Прогресивен', 'Интерактивен',
                    'Корпоративен', 'Международен', 'Продукционен'),
            'zwei': ('Идеи', 'Групи', 'Данни', 'Екипи', 'Марки', 'Мрежи',
                     'Пазари', 'Отговори', 'Решения', 'Тактики', 'Фактори', 'Интранет',
                     'Качество', 'Операции', 'Програми', 'Директиви', 'Маркетинг',
                     'Мобилност', 'Отчетност', 'Парадигми', 'Прилагане', 'Резонанси',
                     'Сигурност', 'Брандиране', 'Интеграция', 'Показатели', 'Приложения',
                     'Въздействие', 'Идентичност', 'Изследвания', 'Комуникации',
                     'Креативност', 'Оптимизация', 'Осигуряване', 'Конфигурации',
                     'Използваемост', 'Взаимодействия', 'Функционалности',
                     'Инфраструктурата'),
            'trois': ('Агент', 'Плановик', 'Техник', 'Инженер', 'Стратег',
                      'Архитект', 'Асистент', 'Дизайнер', 'Директор', 'Мениджър',
                      'Началник', 'Служител', 'Посредник', 'Продуцент', 'Синергист',
                      'Сътрудник', 'Анализатор', 'Изпълнител', 'Консултант', 'Специалист',
                      'Координатор', 'Оркестратор', 'Разработчик', 'Супервайзор',
                      'Фасилитатор', 'Представител', 'Проектант', 'Администратор'),
            'conjunction': ('на', 'по')
        }
}


def random_pretentious_job_title(size: int = 1, number_of_words=3, language: str = 'English'):
    """Generates pretentious job titles with specified number of words and language."""
    mnumber_of_words = number_of_words
    if not (isinstance(number_of_words, type(None)) or isinstance(number_of_words, int) and 0 < number_of_words < 4):
        raise TypeError("The argument 'number-of-words' is expected to be one of 1, 2, 3, or None. Continue using 3.")
        mnumber_of_words = 3
        return None

    mlanguage = language
    if isinstance(mlanguage, str):
        mlanguage = mlanguage.lower()

    if not (mlanguage in set(pretentiousJobTitleWords.keys()) or mlanguage is None):
        warnings.warn(
            "The argument 'language' is expected to be one of 'Bulgarian', 'English', or None. Continuing with 'English'.",
            UserWarning)
        mlanguage = 'English'.lower()

    if not size > 0:
        warnings.warn("The argument 'size' is expected to be non-negative integer.", UserWarning)
        return None

    phrases = []

    for i in range(size):

        n = mnumber_of_words
        if mnumber_of_words is None:
            n = random.choice([1, 2, 3])

        lang = mlanguage
        if lang is None:
            lang = random.choice(list(pretentiousJobTitleWords.keys()))

        r_title = [random.choice(pretentiousJobTitleWords[lang]['uno']),
                   random.choice(pretentiousJobTitleWords[lang]['zwei']),
                   random.choice(pretentiousJobTitleWords[lang]['trois'])]

        if lang == "bulgarian":

            conj = random.choice(pretentiousJobTitleWords[lang]["conjunction"])

            if n == 2:
                r_title = [r_title[2], conj, r_title[1]]
            elif n == 3:
                r_title = [r_title[0], r_title[2], conj, r_title[1]]
            else:
                r_title = [r_title[2], ]

            phrases = phrases + [' '.join(r_title)]

        else:

            r_title = r_title[3 - n:3]
            phrases = phrases + [' '.join(r_title)]

    if size == 1:
        return phrases[0]
    return phrases
