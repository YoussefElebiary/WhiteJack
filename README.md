# ♠️ WhiteJack — A Modern Take on Blackjack (Educational Project)

**WhiteJack** is a clean and modern Blackjack game built with **Python** and **Pygame**.  
It aims to recreate the casino experience for **educational and entertainment purposes only** — no gambling, no real money.  

![WhiteJack](assets/icon.png)

---

## 🎮 Features

- Classic Blackjack rules (Hit, Stand, Double, Split)  
- Realistic dealer logic  
- Multiple hands (splits) supported  
- Balance tracking across rounds  
- Dynamic button-based controls  
- Fully modular, clean code structure  
- Works on Windows, macOS, and Linux  

---

## ⚙️ Installation

### Requirements
- Python 3.9+  
- Pygame library  

### Run from source
Install dependencies and run the main file directly:  
```bash
pip install pygame
python main.py 
```

### Build (optional)
To build a standalone executable using PyInstaller:  
```bash
pyinstaller --noconfirm --onefile --windowed --icon "assets/icon.ico" --name "WhiteJack" --hidden-import "pygame" --add-data "assets;assets/" main.py
```

The compiled version will appear in the `output/` folder as `WhiteJack.exe`.  

---

## 🃏 Assets

Card graphics used in this project are from:  
➡️ [hayeah/playing-cards-assets](https://github.com/hayeah/playing-cards-assets)  

These assets are licensed under the **MIT License**, and full credit goes to the original creator.  
Cards have been adapted for use in this educational project.  

---

## ⚠️ Disclaimer

**This project does not condone, encourage, or support gambling in any form.**

WhiteJack is strictly intended for:
- Educational purposes  
- Personal entertainment  
- Demonstrating Pygame and Python game development  

Any attempt to use this project or its derivatives for real-money gambling, betting, or other financial risk activities is **strictly prohibited** and **entirely at the user's own risk**.  

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.  

> **Note:** The game uses card assets from [hayeah/playing-cards-assets](https://github.com/hayeah/playing-cards-assets), which are also under the MIT License.

---

### 💡 Author

Developed by **Youssef Elebiary**  
Built with ❤️ in Python using Pygame.  

---

> ⚠️ *Remember: Gambling is a serious issue that can lead to addiction and financial harm. This project is designed to promote programming and game development, not betting.*