# Gateway on board

This project contains all configs sources and useful tools to run seanatic gateway project on board (tested on raspberry pi and solidrun solidense board).

## Project schema

![schemas gateway on board](./docs/img/project_schema.png)

`Modbus-binding` will get data from the automate linked in modbus through TCP socket. The `plugin-modbus-seanatic`, a  `signal-composer-binding`'s _plugin_, is here to get data from the modbus-binding, decrypt, and send them to `redis-tsdb-binding` which it will store them into a database. `Cloud-publication-binding` will be configured to take appropriate classes from the redis database and communicate with the this peer through the cloud.

## configs

In the folder **configs**, there are configurations for bindings:

* modbus-binding
* cloud-publication-binding

## binary

You will find a binary into the folder **bin** called *seanatic-gateway*. IT can setup/start and stop all necessary services to process the seanatic gateway project.

```bash
seanatic-gateway [ --start ][ --stop ][--no-security][ -h | --help ]
    - start: Start all gateway services
    - stop: Stop all services
    - no-security (optional): Use 'afb-binder' instead of 'afm-util'
```

## service systemd

It comes with a systemd service which just run the binary to startup easily the project

```bash
systemctl enable seanatic-gateway
systemctl start seanatic-gateway
systemctl status seanatic-gateway
```

## Database

To verify if workflow up to redis works, we can use this 2 command-line:

* To retrieve the last value of each sensor, run in a terminal:

    ```bash
    redis-cli -c TS.MGET FILTER class=ANA
    1) 1) "ANA[0]"
   2) (empty list or set)
   3) 1) (integer) 1642431058052
      2) 1
    2) 1) "ANA[1]"
    2) (empty list or set)
    3) 1) (integer) 1642431058052
        2) 1
    3) 1) "ANA[2]"
    2) (empty list or set)
    3) 1) (integer) 1642431058051
        2) 1
    4) 1) "ANA[3]"
    2) (empty list or set)
    3) 1) (integer) 1642431058051
        2) 1
    5) 1) "ANA[4]"
    2) (empty list or set)
    3) 1) (integer) 1642431058051
        2) 1
    6) 1) "ANA[5]"
    2) (empty list or set)
    3) 1) (integer) 1642431058051
        2) 1
    7) 1) "ANA[6]"
    2) (empty list or set)
    3) 1) (integer) 1642431058050
        2) 0
    8) 1) "ANA[7]"
    2) (empty list or set)
    3) 1) (integer) 1642431058050
        2) 1
    ```

* To see the whole database content, run the following command:

    ```bash
    redis-cli -c TS.MRANGE - + FILTER class=ANA
    1) 1) "ANA[0]"
    2) (empty list or set)
    3)  1) 1) (integer) 1642431048840
            2) 1
        2) 1) (integer) 1642431049052
            2) 0
        3) 1) (integer) 1642431049303
            2) 0
        4) 1) (integer) 1642431049552
            2) 0
        5) 1) (integer) 1642431049803
            2) 0
        6) 1) (integer) 1642431050052
            2) 1
    # [...]
    2) 1) "ANA[1]"
    2) (empty list or set)
    3)  1) 1) (integer) 1642431048839
            2) 1
        2) 1) (integer) 1642431049051
            2) 0
        3) 1) (integer) 1642431049303
            2) 1
        4) 1) (integer) 1642431049552
            2) 1
        5) 1) (integer) 1642431049802
            2) 1
        6) 1) (integer) 1642431050052
            2) 1
    # [...]
    ```
