import os

ENV_FILENAME=".env"
ENV_CONTENT="DATABASE_URL=sqlite://RedInk.db\n"

def create_env_file():
    if os.path.exists(ENV_FILENAME):
        print("The .env was already created and configured.")
        return 0

    with open(ENV_FILENAME, "w") as f:
        f.write(ENV_CONTENT)

    print("The .env file has been correctly created and configured.")

if __name__=="__main__":
    print("Setup of RedInk's database environment...")
    create_env_file()
