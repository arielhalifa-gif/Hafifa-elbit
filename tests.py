import asyncio
import time

# async def say_hello():
#     await asyncio.sleep(1)
#     return "hello"


# async def main():
#      result = await say_hello()
#      return result

# print(asyncio.run(main()))


# 2
# async def work(name, delay):
#     print(f"start {name}")
#     await asyncio.sleep(delay)
#     print(f"end {name}")


# async def main():
#     print(f'start 1 {time.time()}')
#     await asyncio.gather(work("a", 4),
#                          work('b', 2),
#                          work('c', 3))
#     print(f'end 1 {time.time()}')

#     print(f'start 2 {time.time()}')
#     await work("a", 4)
#     await work('c', 3)
#     await work('b', 2)
#     print(f'end 2 {time.time()}')


# asyncio.run(main())



# async def counter():
#     for i in range(1, 6):
#         await asyncio.sleep(0.5)
#         yield i

# async def main():
#     async for num in counter():
#         print(num)

# asyncio.run(main())



# async def risky(n):
#     if n == 2:
#         raise Exception("boom")
#     return n * 2

# async def main():
#     results = await asyncio.gather(
#         risky(1),
#         risky(2),
#         risky(3),
#         return_exceptions=True
#     )

#     for r in results:
#         print(r)

# asyncio.run(main())



# async def slow():
#     await asyncio.sleep(3)

# async def main():
#     try:
#         await asyncio.wait_for(slow(), timeout=1)
#     except asyncio.TimeoutError:
#         print("timeout!")

# asyncio.run(main())


from datetime import datetime, timedelta

# start point (you can change this)
start_time = datetime(2024, 1, 1, 0, 0, 0)

# how many hours
n = 100

# output file
output_file = "test_dates.txt"

with open(output_file, "w") as f:
    for i in range(n):
        dt = start_time + timedelta(hours=i)
        f.write(dt.strftime("%Y-%m-%d %H:%M:%S") + "\n")

print(f"Generated {n} hourly dates → {output_file}")