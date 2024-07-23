

class Transformers():
    """
    this class transform the obj as requested
    Strip decorator ensures all strings are being stripped
    """

    def Strip(func):
        def wrapper(text):
            try:
                stripped_text = text.strip()
                return func(stripped_text)
            except Exception as e:
                print(f"Exception occurred in {func.__name__}: {str(e)}")
                return text

        return wrapper

    @Strip
    @staticmethod
    def basic_strip_transform(obj):
        return obj

    @Strip
    @staticmethod
    def lowercase_email_transformer(obj):
        try:
            return obj.lower()
        except:
            return obj

    @Strip
    @staticmethod
    def phone_regex_transformer(obj):
        """
        regardless of the pattern, divide into 2 parts such that 0##-#######
        :param obj:
        :return:
        """
        if obj[0] == '0':
            return f"{obj[:3]}-{obj[3:len(obj)].replace('-', '')}"
        else:
            return obj
