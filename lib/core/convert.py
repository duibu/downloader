def getUnicode(value, encoding=None, noneToNull=False):
    """
    Returns the unicode representation of the supplied value

    >>> getUnicode('test') == u'test'
    True
    >>> getUnicode(1) == u'1'
    True
    >>> getUnicode(None) == 'None'
    True
    """

    if noneToNull and value is None:
        return NULL

    if isinstance(value, six.text_type):
        return value
    elif isinstance(value, six.binary_type):
        # Heuristics (if encoding not explicitly specified)
        candidates = filterNone((encoding, kb.get("pageEncoding") if kb.get("originalPage") else None, conf.get("encoding"), UNICODE_ENCODING, sys.getfilesystemencoding()))
        if all(_ in value for _ in (b'<', b'>')):
            pass
        elif any(_ in value for _ in (b":\\", b'/', b'.')) and b'\n' not in value:
            candidates = filterNone((encoding, sys.getfilesystemencoding(), kb.get("pageEncoding") if kb.get("originalPage") else None, UNICODE_ENCODING, conf.get("encoding")))
        elif conf.get("encoding") and b'\n' not in value:
            candidates = filterNone((encoding, conf.get("encoding"), kb.get("pageEncoding") if kb.get("originalPage") else None, sys.getfilesystemencoding(), UNICODE_ENCODING))

        for candidate in candidates:
            try:
                return six.text_type(value, candidate)
            except (UnicodeDecodeError, LookupError):
                pass

        try:
            return six.text_type(value, encoding or (kb.get("pageEncoding") if kb.get("originalPage") else None) or UNICODE_ENCODING)
        except UnicodeDecodeError:
            return six.text_type(value, UNICODE_ENCODING, errors="reversible")
    elif isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value
    else:
        try:
            return six.text_type(value)
        except UnicodeDecodeError:
            return six.text_type(str(value), errors="ignore")