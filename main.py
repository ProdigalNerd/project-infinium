from console.terminal import Terminal
from game.database.base import Base
from game.database.session import engine

def main():
    Base.metadata.create_all(bind=engine)
    Terminal().run()

if __name__ == "__main__":
    main()
