import vindinium


def main():

    #while True:
        # Create a vindinium client
        client = vindinium.Client(
            server = "http://vindinium.org",
            key = "",
            mode = "training",
            n_turns = 300,
            open_browser = True
        )

        url = client.run(vindinium.bots.MinerBot())
        print 'Replay in:', url

if __name__ == '__main__':
    main()
