
function install_app() {
  shell_type="$1"
  app="$2"
  user_name="$3"

  if ! [[ -x "$(command -v sudo -u "$user_name" $app)" ]] || [[ -x "$(command -v $app)" ]]; then
    echo "$app is not installed. Installing $app" >&2
    if [[ $shell_type == "zsh" ]]; then
      echo "Installing with brew"
      sudo -u "$user_name" brew install $app
    else
      echo "Installing with apt-get"
      apt-get install $app
    fi
  else
    echo "$app is already installed"
  fi
}

user_name="$1"
shell_type="$(bash --version)"
port="50100"
config_path="$(pwd)/config/config.json"

echo "Installing python requirements"
#pip install -r requirements.txt

if [[ $shell_type =~ "apple" ]]; then
  echo "Using zsh"
  install_app "zsh" "redis" $user_name
else
  echo "Using bash"
  install_app "bash" "redis"
fi

echo "Starting redis-server"
redis-server &

echo "Starting AutoDownloader App"
if [[ $shell_type =~ "apple" ]]; then
  ip_address="$(ipconfig getifaddr en0)"
else
  ip_address="$(ipconfig getifaddr en0)"
fi
#bash

