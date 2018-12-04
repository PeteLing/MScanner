# coding=utf8
import threading
import time

num = 0
lock1 = threading.Lock()
lock2 = threading.RLock()


def sum_num1(i):
    global num
    time.sleep(1)
    num += i
    print(num)


def sum_num2(i):
    lock1.acquire()
    global num
    time.sleep(1)
    num +=i
    print(num)
    lock1.release()


def sum_num3(i):
    lock2.acquire()
    global num
    lock2.acquire()
    time.sleep(1)
    num +=i
    lock2.release()
    print(num)
    lock2.release()


if __name__ == '__main__':
    print('%s thread start!' % (time.ctime()))
    try:
        for i in range(6):
            t = threading.Thread(target=sum_num3, args=(i,))
            t.start()

    except KeyboardInterrupt as e:
        print("you stop the threading")

    print('%s thread end!' % (time.ctime()))
