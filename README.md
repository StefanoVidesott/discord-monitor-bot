# discord-monitor-bot

remember to create the file `.env` in the root directory with the following content:

```
BOT_TOKEN=<your_bot_token>
```

## Running the bot locally

```bash
docker compose up
```

## Running the bot on a server

```bash
ssh -f <name>@<server_ip> "docker compose -f /home/stefano/it/discord-monitor-bot/docker-compose.yml up"
```

## Stopping the bot on a server

```bash
ssh -f <name>@<server_ip> "docker compose -f /home/stefano/it/discord-monitor-bot/docker-compose.yml down"
```
