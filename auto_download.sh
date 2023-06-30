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
      exit 1
    fi
  fi
  echo "$python_cmd" "$pip_cmd"
}

# Check the number of arguments
if [ $# -lt 1 ]; then
    echo -e "\nUsage: $0 <username>\nExiting...\n"
    exit 1
fi

# Assign arguments to variables
user_name="$1"
shell_type="$(bash --version)"
port="5000"
script_dir=$(dirname "$(readlink -f "$0")")
config_path="$script_dir/config/config.json"

# Validate config.json file exists
if [ ! -e "$config_path" ]; then
    echo -e "\nconfig.json file not found at: $config_path\n"
    echo -e "Please check the file path and try again.\nExiting...\n"
    exit 1
fi

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
logs_folder="$(cat $config_path | jq -r ".user_preferences.logs_folder")"
echo "Creating logs folder $logs_folder"
mkdir -p "$logs_folder"

echo "Starting redis-server"
redis-server &

echo "Starting AutoDownloader App $ip_address:$port"
"$python_cmd" app.py "$config_path" "$port" "$ip_address"

