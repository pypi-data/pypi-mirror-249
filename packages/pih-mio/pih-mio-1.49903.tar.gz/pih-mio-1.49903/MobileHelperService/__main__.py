def start() -> None:
    from MobileHelperService.service import MobileHelperService, checker
    MobileHelperService(10, checker).start()

if __name__ == '__main__':
    start()
