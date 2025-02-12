from falcons_stats.scripts.scraper import Scraper

def main():
    scraper = Scraper()
    goal_scorers = scraper.get_goal_scorers()
    # print(goal_scorers)
    print(goal_scorers.keys())
    
if __name__ == "__main__":
    main()

