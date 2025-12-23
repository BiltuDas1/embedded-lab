# Embedded Lab

A personal collection of embedded systems experiments, code snippets, and learning resources. This repository serves as a log of my progress, a reference for past work, and a source of motivation to see how far I've come.

- [Embedded Lab](#embedded-lab)
  - [How to use](#how-to-use)
  - [How to compile](#how-to-compile)
  - [FAQ](#faq)
    - [Board Not Found](#board-not-found)

## How to use

- Clone this repo

  ```bash
  git clone https://github.com/BiltuDas1/embedded-lab
  ```

- Download [Arduino CLI](https://docs.arduino.cc/arduino-cli/installation/)
- Set the Arduino CLI in Path, and done

## How to compile

- Connect your MCU (Microcontroller Unit) with PC
- Open Terminal
  - If Windows then open Powershell and enter:

    ```powershell
    . ./tools/source.ps1
    ```

  - If Unix/Linux based system then enter:

    ```bash
    source ./tools/source.sh
    ```

- Get Port of the connected MCU

  ```bash
  arduino-cli board list
  ```

- Create a `config.env` file at the root and then keep the `Port` value like this:
  ```env
  PORT=COM4
  ```
- Now enter the command to list all the boards
  ```bash
  arduino-cli board listall
  ```
- Now choose the MCU from the list and note down the `FQBN`, and then store the value to the `config.env` file like this

  ```env
  PORT=COM4
  BOARD_ID=esp8266:esp8266:generic
  ```

  > If the specific device is not found then [see here](#board-not-found)

- Now for compiling use the command
  ```bash
  cross-compiler . # For compiling current directory
  ```
  ```bash
  cross-compiler src/blink_led # For compiling a specific directory
  ```
- After the compilation done, use this to push the code to MCU
  ```bash
  cross-compiler --upload
  ```

## FAQ

### Board Not Found

- If the board not found then add the board URL like this
  ```bash
  arduino-cli config add board_manager.additional_urls http://arduino.esp8266.com/stable/package_esp8266com_index.json
  ```
- Update the board list
  ```bash
  arduino-cli core update-index
  ```
- Install the device package like this
  ```bash
  arduino-cli core install esp8266:esp8266
  ```
- Now the device will be visible in the list
