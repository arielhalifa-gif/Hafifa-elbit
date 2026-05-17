def count():
    yield 1
    yield 2
    yield 3

g = count()

print(count())  # 1
print(g)  # 2
print(g)  # 3