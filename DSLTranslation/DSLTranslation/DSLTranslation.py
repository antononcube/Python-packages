import json
import urllib.request
import pyperclip
import warnings

warnings.formatwarning = lambda msg, *args, **kwargs: f'{msg}\n'

def dsl_web_service_interpretation_url(command,
                                       url="http://accendodata.net:5040/translate",
                                       sub='',
                                       to_language="Python",
                                       from_langauge="English"
                                       ):
    command_safe = urllib.parse.quote(command)

    urlLocal = url

    if len(sub) > 0:
        urlLocal = url + "/" + sub

    url_safe = urlLocal + "?command=" + command_safe + "&lang=" + to_language + "&from-lang" + from_langauge

    return url_safe


def dsl_web_service_interpretation(command,
                                   url="http://accendodata.net:5040/translate",
                                   sub='',
                                   to_language="Python",
                                   from_langauge="English"
                                   ):
    url_safe = dsl_web_service_interpretation_url(command=command,
                                                  url=url,
                                                  sub=sub,
                                                  to_language=to_language,
                                                  from_langauge=from_langauge
                                                  )

    # "http://accendodata.net:5040/translate?command=make%20a%20document%20term%20matrix&lang=WL&from-lang=Automatic"

    data = urllib.request.urlopen(url_safe).read()
    res = json.loads(data)
    return res


def dsl_translation(command: str,
                    url: str = "http://accendodata.net:5040/translate",
                    sub: str = '',
                    to_language: str = "Python",
                    from_langauge: str = "English",
                    fmt: str = "code",
                    fallback: bool = True,
                    copy_to_clipboard: bool = True
                    ):
    """
    DSL translation
    ---------------

    :param command: Command to translate.
    :param url: Web service URL.
    :param sub: Sub for given URL.
    :param to_language: Language to translate to: one of 'Bulgarian', 'English', 'Python', 'R', 'Raku', 'Russian', or 'WL';
    :param from_langauge: Language to translate from; one of 'Bulgarian', 'English', or 'Whatever'.
    :param fmt: Format of the result; one of 'json', 'dict', 'code';
    :param fallback: Timeout in seconds.
    :param copy_to_clipboard: Copy to clipboard command.
    :return: A dictionary or a string
    """
    res = dsl_web_service_interpretation(command=command,
                                         url=url,
                                         sub=sub,
                                         to_language=to_language,
                                         from_langauge=from_langauge
                                         )

    if len(res["CODE"]) == 0 and fallback:
        warnings.warn("Making a fallback call with the question answering system.", stacklevel=-1)
        return dsl_translation(command=command,
                               url=url,
                               sub='qas',
                               to_language=to_language,
                               from_langauge=from_langauge,
                               fmt=fmt,
                               fallback=False,
                               copy_to_clipboard=copy_to_clipboard
                               )

    resCB = json.dumps(res)
    if fmt.lower() == "code":
        if len(res["CODE"]) == 0:
            warnings.warn("Empty code result.")
        res = res["CODE"]
        resCB = res

    if copy_to_clipboard:
        pyperclip.copy(resCB)

    return res
