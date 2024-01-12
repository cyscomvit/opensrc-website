# opensrc-website

CYSCOM VIT's leaderboard hosted [here](https://opensrc.cyscomvit.com)

# Setup

1. Place a `.env` file in this same folder [here](./.env)

    Format of `.env` file

    ```{env}
    START_ACT=
    END_ACT=
    CURRENT_ACT_YEAR=
    FIREBASE_DB=
    FIREBASE_STORAGE=
    DEBUG=
    ```

2. Run using docker
    ```{sh}
    docker build -t cyscomvit/opensrc-website:latest .
    docker run --detach --publish 5000:5000 --name opensrc-website-deploy cyscomvit/opensrc-website:latest
    ```
