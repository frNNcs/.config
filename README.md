# Configuration repo

## Install zsh
```
# linux
sudo apt-get install zsh

# Macos
brew install zsh
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