import vindinium


def main():

    #while True:
        # Create a vindinium client
        client = vindinium.Client(
            server = "http://vindinium.org",
            key = "3z0j970e",   #jbot04
            mode = "arena",
            n_turns = 300,
            open_browser = False
        )

        props = {"mine" : 10.0,
                 "drink": 2.0,
                 "kill" : 1.0,
                 "flee" : 2.0}

        url = client.run(vindinium.bots.DecisionBot(props))
        print 'Replay in:', url

if __name__ == '__main__':
    main()