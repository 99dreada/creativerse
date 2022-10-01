from functools import wraps

def create_forms(*forms):
    def _inner(f):
        @wraps(f)
        def _wrapper(*args,**kwargs):
            def create_bot_form(**kwargs):
                bot_form = Bot_Form(request.form)
                return bot_form
            mapping = {'bot_form': create_bot_form,
                      }
            formObjs = {}
            for form in forms:
                formObjs[form] = mapping[form](**kwargs)
            return f(*args, forms=formObjs, **kwargs)
        return _wrapper
    return _inner