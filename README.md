# TfNSW Departure Bot
This project creates a Discord bot using Python that fetches transit departure information from TfNSW’s Open Data API and displays real-time departure from Redfern Station for University of Sydney community on discord. Users can also use command to query departure information of any station/stop available in the Open Data API.

This project includes a docker image file that can be used to build a container image. You can start the bot using the included docker-compose

## Feature
Automatically updated Redfern Station departure display <br><br>
![image](https://user-images.githubusercontent.com/39119527/134812794-7e9d0af9-5c59-483c-b617-b3a7bc4efd0c.png)


`!departure [station]` command <br><br>
![image](https://user-images.githubusercontent.com/39119527/134812855-da75abca-4617-4796-a95e-303fb9e9af26.png) <br><br>
![image](https://user-images.githubusercontent.com/39119527/134812884-1f8b813a-cfb7-4ee6-8eb9-8c08e3f35e29.png)




## Prerequisite
- Docker
- Docker-compose



## Usage
1. Provide Discord developer API for bot account and TfNSW Open Data API for departure data in `env.py`
2. Start the bot with `docker-compose up -d`

