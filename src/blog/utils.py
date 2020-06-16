import random
import string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
