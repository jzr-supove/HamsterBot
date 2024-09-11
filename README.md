# HamsterBot 🐹

HamsterBot automates mini-game playing, promocode generation, and application for Hamster Kombat on Telegram, offering undetectable and fully automated gameplay enhancement.

## ⭐ Key Features

- Automates mini-game playing in Hamster Kombat
- Generates and applies promo codes authentically
- "Fire and forget" functionality

## 🔥 Why this HamsterBot among others?

- **Undetectable**: Emulates legitimate gameplay using proper API interactions
- **Fully Automated**: Continuous operation without user intervention
- **Safe**: Generates keys organically, reducing detection risk

## 📥 Installation & Setup

1. Clone the repository to your local filesystem:
    ```sh
    git clone https://github.com/jzr-supove/HamsterBot.git
    cd ./HamsterBot
    ```
2. Create a virtual environment (optional, but recommended):
    ```sh
    python -m venv venv
    . venv\Scripts\activate # On Ubuntu use `source venv/bin/activate`
    ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create `config.ini` configuration file (from `config.ini.example` file provided)
    ```sh
    cp config.ini.example config.ini
    ```

5. Fill the configuration file with your data:
    - `AUTH_TOKEN` - Your auth token
    - `SEC_CH_UA`, `USER_AGENT` - Your browser headers
    
    > See the [Configuration](#Configuration) section for how to obtain them

6. Run the emulator:
    ```sh
    python main.py
    ```

## Usage

1. Make sure you are in project directory
2. *\(Optional\)* Activate the virtual environment if you set one up during installation
3. Run the script:
   ```sh
    python main.py
    ```

## Configuration

### Obtaining your `AUTH_TOKEN`

> *Video guide will be available soon*

#### Manually, using DevTools:

1. Login to your telegram account through [web](https://web.telegram.org) version of Telegram 
2. Open DevTools (F12), switch to Network tab
3. Inspect hamster kombat related requests and copy `Authorization` header value starting with `Bearer`

#### (SOON) Automatically, using extension:
- > Extension is being developed, and will be available soon. 
- > Good at making browser extensions? Feel free to make a Pull Request
1. Login to your telegram account through [web](https://web.telegram.org) version of Telegram
2. Install the extension and enable it, it will get auth token automatically for you
3. Launch the game
4. Open extension popup and copy your token

### Obtaining `SEC_CH_UA` and `USER_AGENT` (optional):
For getting your browser headers, visit https://modheader.com/headers inside Telegram on your phone (using built-in Telegram browser), 
and copy `user-agent` and `sec-ch-ua` header values to `config.ini` file.

## 🔥 Upcoming Updates:

- [ ] AFK Farm - farms coins 24/7 
- [ ] Optimal Auto-Upgrade - calculates and buys the most efficient upgrade card

## 💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Please support the project by giving it a star ⭐️

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📨 Community

- Telegram: [@JZRLog](https://t.me/jzrlog)

## ⚠️ Disclaimer

This project is for educational purposes only. Please use responsibly and in accordance with the terms of service of any games you may use it with.