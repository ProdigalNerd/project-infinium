from dotenv import load_dotenv
from console.terminal import Terminal
from game.database.base import Base
from game.database.session import engine

load_dotenv()

def main():
    Base.metadata.create_all(bind=engine)
    Terminal().run()

if __name__ == "__main__":
    main()
