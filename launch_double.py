import vindinium

def main():
    # Create a vindinium client
    client = vindinium.Client(
        server = "http://vindinium.org",
        key = "8ts7e6fp",
        mode = "arena",
        n_turns = 300,
        open_browser = True
    )

    url = client.run(vindinium.bots.HunterBot())
    print 'Replay in:', url

    # Create number 2
    client = vindinium.Client(
        server = "http://vindinium.org",
        key = "h7dyy1cl",
        mode = "arena",
        n_turns = 300,
        open_browser = True
    )

    url = client.run(vindinium.bots.HunterBot())
    print 'Replay in:', url

if __name__ == '__main__':
    main()
