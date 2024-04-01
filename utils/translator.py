# 20230619
import traceback
import translators
import config


def translate(line: str, source_lang: str = 'auto', target_lang: str = config.Config.translate_to) -> str:
    result = config.Config.translate_fail_action
    try:
        result = translators.translate_text(line,
                                            translator=config.Config.translate_api[0],
                                            from_language=source_lang,
                                            to_language=target_lang)
        if isinstance(result, str):
            return result
        if isinstance(result, dict):
            # should parse dict here
            raise NotImplementedError
    except NotImplementedError:
        raise
    except Exception:
        print(traceback.format_exc())
        return result


if __name__ == "__main__":
    test_text = "tonight, we have dinner in the KFC"
    r = translators.translate_text(test_text,
                                   translator='sogou',
                                   from_language='auto',
                                   to_language='zh')
    print(r)
