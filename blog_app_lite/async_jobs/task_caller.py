from tasks import add 
result = add.delay(4, 4)

print(result.get(timeout=1))
print(result.ready())