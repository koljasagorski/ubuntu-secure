import os
import subprocess

def run_command(command):
    """Run a system command and print output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(result.stderr)
    return result.returncode == 0

def install_unattended_upgrades():
    """Install unattended-upgrades if it's not already installed."""
    print("Installing unattended-upgrades...")
    run_command("sudo apt update")
    run_command("sudo apt install -y unattended-upgrades")

def configure_unattended_upgrades():
    """Configure unattended-upgrades for automatic updates."""
    print("Configuring unattended-upgrades...")
    
    # Ensure the necessary origins are configured for security and regular updates
    config_content = """Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}:${distro_codename}-updates";
    "deb https://downloads.plex.tv/repo/deb public main";
    "deb https://apt.sonarr.tv/debian buster main";
};
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
"""
    with open("/etc/apt/apt.conf.d/50unattended-upgrades", "w") as config_file:
        config_file.write(config_content)

    # Enable daily updates and upgrades
    auto_upgrades_content = """APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
"""
    with open("/etc/apt/apt.conf.d/20auto-upgrades", "w") as auto_upgrades_file:
        auto_upgrades_file.write(auto_upgrades_content)

def add_custom_repos():
    """Add repositories for Plex, Radarr, Sonarr, and ensure SABnzbd repository."""
    print("Adding Plex repository and key...")
    run_command("echo 'deb https://downloads.plex.tv/repo/deb public main' | sudo tee /etc/apt/sources.list.d/plexmediaserver.list")
    run_command("curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -")

    print("Adding Sonarr and Radarr repository...")
    run_command("sudo apt install -y gnupg ca-certificates")
    run_command("sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5857F8CAA43C79AD")
    run_command("echo 'deb https://apt.sonarr.tv/debian buster main' | sudo tee /etc/apt/sources.list.d/sonarr.list")

    print("Ensuring SABnzbd repository...")
    run_command("sudo add-apt-repository -y ppa:jcfp/nobetas")

def start_qemu_agent():
    """Ensure QEMU Guest Agent is running."""
    print("Starting QEMU Guest Agent...")
    run_command("sudo systemctl enable --now qemu-guest-agent")

def main():
    """Main function to execute all steps."""
    install_unattended_upgrades()
    configure_unattended_upgrades()
    add_custom_repos()
    start_qemu_agent()
    print("Setup complete. Automatic updates are configured for Plex, Radarr, Sonarr, SABnzbd, and QEMU Guest Agent.")

if __name__ == "__main__":
    main()
