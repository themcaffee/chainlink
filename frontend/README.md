# Chainlink Frontend

The web frontend to the chainlink API. Handles getting github packages and 
directly getting issues from the github API.

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn run serve
```

### Compiles and minifies for production
```
yarn run build
```

### Run your tests
```
yarn run test
```

### Lints and fixes files
```
yarn run lint
```


### Setting up AWS S3 + Cloudfront + Gitlab CI

- Create s3 buckets
- Setup cloudfront for buckets
- (Optional) Setup Route 53 to cloudfront
- Get S3 CLI credentials
- Create gitlab CI environment variables with S3 creds
- Create .gitlab-ci.yml with proper stages
