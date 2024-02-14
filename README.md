# Configuration repo

## Install zsh
``` bash
# linux
sudo apt-get install zsh

# Macos
brew install zsh

# ln -s ~/.config/.zshrc ~/.zshrc
# ln -s ~/.config/.p10k.zsh ~/.p10k.zsh
```

## Install OhmyZsh
```bash
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```


## Install powerlevel10k

``` bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

## Pyenv

```bash
curl https://pyenv.run | bash
```

## Nvm

```bash
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```
