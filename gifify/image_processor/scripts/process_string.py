def process_string(str):

    return str.replace(" ", "_")\
                .replace("[", "")\
                .replace("]", "")\
                .replace("(", "")\
                .replace(")", "")\
                .replace("{", "")\
                .replace("}", "")\
                .replace("'", "")\
                .replace('"', "")\
                .replace('!', "")\
                .replace('?', "")\
                .replace(',', "")\
                .replace('@', "")\
                .replace('#', "")\
                .replace('$', "")\
                .replace('%', "")\
                .replace('^', "")\
                .replace('&', "")\
                .replace('*', "")\
                .replace('<', "")\
                .replace('>', "")\
                .replace('+', "")\
                .replace('*', "")\
                .replace("|", "")
