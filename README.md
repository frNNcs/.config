# Configuration repo

## Install zsh
``` bash
# linux
sudo apt-get install zsh

# Macos
brew install zsh

# ln -s ~/.config/.zshrc ~/.zshrc
```

## Install OhmyZsh
```bash
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# ln -s ~/.config/.oh-my-zsh-custom /home/frnn/.oh-my-zsh/custom
```


## Install powerlevel10k

``` bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
# ln -s ~/.config/.p10k.zsh ~/.p10k.zsh

```

## Pyenv

```bash
curl https://pyenv.run | bash
```

## Nvm

```bash
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```
