from finger.FingerScan import FingerScan


if __name__ == '__main__':
    fs = FingerScan()
    url = "www.baidu.com"
    test = fs.scan_finger(url)
    for item in test:
        print(item)
    print(fs.get_server())