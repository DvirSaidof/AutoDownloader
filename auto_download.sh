#function install_app() {
#  shell_type="$1"
#  app="$2"
#  user_name="$3"
#
#  if ! [[ -x "$(command -v sudo -u "$user_name" $app)" ]] && ! [[ -x "$(command -v $app)" ]]; then
#    echo "$app is not installed. Installing $app" >&2
#    if [[ $shell_type == "zsh" ]]; then
#      echo "Installing with brew"
#      sudo -u "$user_name" brew install $app
#    else
#      echo "Installing with apt-get"
#      apt install $app
#    fi
#  else
#    echo "$app is already installed"
#  fi
#}

function install_app() {
  shell_type="$1"
  app="$2"
  user_name="$3"

  if ! type "$app" || ! sudo -u "$user_name" type "$app"; then
    echo "$app is not installed. Installing $app" >&2
    if [[ $shell_type == "zsh" ]]; then
      echo "Installing with brew"
      yes | sudo -u "$user_name" brew install $app
    else
      echo "Installing with apt"
      yes | apt install $app
    fi
  else
    echo "$app is already installed"
  fi
}
function set_python_env() {
  python_cmd="python"
  pip_cmd="pip"
  if ! type "$python_cmd" &> /dev/null; then
    if type python3 &> /dev/null; then
      python_cmd="python3"
      pip_cmd="pip3"
    else
      echo "Couldn't find python installed in the system"
      exit
    fi
  fi
  echo "$python_cmd" "$pip_cmd"
}

user_name="$1"
shell_type="$(bash --version)"
port="5000"
config_path="$(pwd)/config/config.json"

read python_cmd pip_cmd < <(set_python_env)

echo "Installing python requirements"
"$pip_cmd" install -r requirements.txt

if [[ $shell_type =~ "apple" ]]; then
  echo "Using zsh"
  install_app "zsh" "redis-server" $user_name
  install_app "zsh" "jq" $user_name
  ip_address="$(ipconfig getifaddr en0)"
else
  echo "Using bash"
  install_app "bash" "redis-server" $user_name
  install_app "bash" "jq" $user_name
  ip_address="$(hostname -I)"
fi
logs_folder=$(cat config/config.json | jq ".user_preferences.logs_folder")
echo "Creating logs folder $logs_folder"
mkdir -p "$logs_folder"

echo "Starting redis-server"
redis-server &

echo "Starting AutoDownloader App $ip_address:$port"
"$python_cmd" app.py "$config_path" "$port" "$ip_address"

