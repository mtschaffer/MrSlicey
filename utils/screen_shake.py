def screen_shake(shake_count, shake_magnitude):
    shake_maximum = shake_count * shake_magnitude
    shake_vector = -1

    for i in range(0, shake_count):
        for x in range(0, shake_maximum, shake_magnitude):
            yield (x * shake_vector, 0)
        for x in range(shake_maximum, 0, -shake_magnitude):
            yield (x * shake_vector, 0)
        shake_vector *= -1
    while True:
        yield (0, 0)
