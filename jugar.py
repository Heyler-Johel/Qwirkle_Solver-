if __name__ == '__main__':
    import argparse
    from qwirkle import QwirkleGame

    parser = argparse.ArgumentParser(description='Qwirkle')
    parser.add_argument('--jugadores', nargs='+')

    juego = QwirkleGame()
    juego.main(parser.parse_args().jugadores)