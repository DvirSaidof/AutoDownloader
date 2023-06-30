#!/bin/bash

# Check the number of arguments
if [ $# -lt 1 ]; then
    echo -e "\nMissing user param\nUsage: sudo $0 \$(whoami)\nExiting...\n"
    exit 1
fi
# Set the right shell type
if [[ "$(bash --version)" =~ "apple" ]]; then
  echo "Using zsh shell"
  shell_type="zsh"
else
  echo "Using bash shell"
  shell_type="bash"
fi

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
function install_requirements() {
  shell_type="$1"
  pip_cmd="$2"
  user_name="$3"

  echo "Installing python requirements"
  "$pip_cmd" install -r requirements.txt

  echo "Installing system requirements"
  install_app "$shell_type" "redis-server" "$user_name"
  install_app "$shell_type" "jq" "$user_name"
}
function get_ip_address() {
  shell_type="$1"
  if [[ $shell_type == "zsh" ]]; then
    ip_address="$(ipconfig getifaddr en0)"
  else
    ip_address="$(hostname -I)"
  fi
  echo "$ip_address"
}
function validate_config_file() {
  config_path="$1"
  if [ ! -e "$config_path" ]; then
      echo -e "\nconfig.json file not found at: $config_path\n"
      echo -e "Please check the file path and try again.\nExiting...\n"
      exit 1
  fi
}
function create_log_folder() {
  config_path="$1"
  logs_folder="$(cat $config_path | jq -r ".user_preferences.logs_folder")"
  echo "Creating logs folder $logs_folder"
  mkdir -p "$logs_folder"
}

# Assign arguments to variables
user_name="$1"
port="5000"
script_dir=$(dirname "$(readlink -f "$0")")
config_path="$script_dir/config/config.json"
python_cmd="python"
pip_cmd="pip"
ip_address=""

# Validate config.json file exists
validate_config_file "$config_path"

# Set python and pip versions
read python_cmd pip_cmd < <(set_python_env)
echo "Using $python_cmd and $pip_cmd"

# Install python and system requirements
install_requirements "$shell_type" "$pip_cmd" "$user_name"

# Set the local ip address
read ip_address < <(get_ip_address "$shell_type")
echo "Local IP Address: $ip_address"

# Create the logs folder if doesn't exists
create_log_folder "$config_path"

echo "Starting redis-server"
redis-server &

echo "Starting AutoDownloader App $ip_address:$port"
"$python_cmd" app.py "$config_path" "$port" "$ip_address"

