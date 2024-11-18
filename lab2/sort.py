from cm_tymer import cm_timer_2

data = [4, -30, 100, -100, 123, 1, 0, -1, -4]

if __name__ == '__main__':
    with cm_timer_2:
        result = sorted(data, key=abs, reverse=True)
    print(result)

    with cm_timer_2:
        result_with_lambda = sorted(data, key=lambda x: abs(x), reverse=True)
    print(result_with_lambda)