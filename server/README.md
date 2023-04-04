# Install dependecies
```
make install
```

## Для поднятия в докере нужно установить и запустить его и настроить WSL 2. После этого в терминали прописываете
```
make compose-up
```
## Before start make migrations
```
make migrate-init
```
### Create a new migration
```
make migrate-create
```
### Upgrade tables
```
make migrate-up
```


## Start App
```
make run-backend
```

