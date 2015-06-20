import vindinium

def main():
    # Create a vindinium client
    client = vindinium.Client(
        server = "http://vindinium.org",
        key = "n3c95t32",
        mode = "training",
        n_turns = 300,
        open_browser = True
    )

    url = client.run(vindinium.bots.MinerBot())
    print 'Replay in:', url

if __name__ == '__main__':
    main()
