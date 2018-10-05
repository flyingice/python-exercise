import const

const.NAME = "flyingice"
print(const.NAME)

try:
    const.NAME = "yyang"
except TypeError as err:
    print(err)

try:
    const.name = "yyang"
except TypeError as err:
    print(err)
