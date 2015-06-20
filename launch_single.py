import vindinium

def main():
    # Create a vindinium client
    client = vindinium.Client(
        server = "http://vindinium.org",
        key = "aewjd4k0",
        mode = "arena",
        n_turns = 300,
        open_browser = True
    )

    url = client.run(vindinium.bots.HunterBot())
    print 'Replay in:', url

if __name__ == '__main__':
    main()
