# 20230619
# TODO: move to manager
import traceback
import translators

from utils import CONFIG
from utils.logger import get_logger

logger = get_logger("translate")


def translate(line: str, source_lang: str = 'auto', target_lang: str = CONFIG.Translate.target_language) -> str:
    result = CONFIG.Translate.fail_hint
    try:
        result = translators.translate_text(line,
                                            translator=CONFIG.Translate.api[0],
                                            from_language=source_lang,
                                            to_language=target_lang)
        if isinstance(result, str):
            return result
        if isinstance(result, dict):
            # should parse dict here
            raise NotImplementedError
    except NotImplementedError:
        raise
    except Exception as e:
        logger.warning(f"translate {line} failed {e}, {traceback.format_exc()}")
        return result


if __name__ == "__main__":
    test_text = "tonight, we have dinner in the KFC"
    r = translators.translate_text(test_text,
                                   translator='sogou',
                                   from_language='auto',
                                   to_language='zh')
    print(r)
