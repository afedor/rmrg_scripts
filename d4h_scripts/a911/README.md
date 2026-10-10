# A911 Authentication

## OAuth Generation

https://active911.atlassian.net/wiki/spaces/AED/pages/1866661961/Personal+Test+OAuth+Token+Generation

- Login to active911.com firts
- Then go to `https://console.active911.com/interface/dev/oauth_gen.php` to get a token

## Tokens (New protocol which doesn't work)

https://active911.atlassian.net/wiki/spaces/AED/pages/2018443276/Generating+an+Access+Token

Once a year, need to get a refresh token:
```
curl -X POST https://user-service.active911.com/v1/authenticate -d "email=example@active911.com" -d "password=Password123"
```

Then you can get an access token (Needed every 15 minutes)
```
curl --location --request POST 'https://user-service.active911.com/v1/user/access' \
--header 'Authorization: a911Auth <REFRESH-TOKAN>'
```

