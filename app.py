import requests
import json

# Replace with the Meraki API base URL
BASE_URL = "https://api.meraki.com/api/v1/"

# Function to get the organization's networks and list them
def list_networks(api_key, organization_id):
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
    }
    response = requests.get(f"{BASE_URL}organizations/{organization_id}/networks", headers=headers)

    if response.status_code == 200:
        networks = json.loads(response.text)
        print("Available Networks:")
        for network in networks:
            print(f"ID: {network['id']}, Name: {network['name']}")
        return networks
    else:
        print("Failed to retrieve networks. Please check your API key and organization ID.")
        return None

# Function to get site-to-site VPN information for a selected network
def get_vpn_info(api_key, network_id):
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
    }
    response = requests.get(f"{BASE_URL}networks/{network_id}/appliance/vpn/siteToSiteVpn", headers=headers)

    if response.status_code == 200:
        vpn_info = json.loads(response.text)
        return vpn_info
    else:
        print("Failed to retrieve VPN information for the selected network.")
        return None

# Function to update site-to-site VPN configuration for a selected network
def update_vpn_config(api_key, network_id, vpn_info, hubs_order):
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
    }
    
    # Use the same mode, subnets, and localSubnet as the existing VPN configuration
    vpn_config = {
        "mode": vpn_info["mode"],
        "hubs": []
    }

    # Rearrange the hubs based on user's input and add useDefaultRoute
    for hub_id in hubs_order:
        hub = {
            "hubId": hub_id,
            "useDefaultRoute": vpn_info["hubs"][0]["useDefaultRoute"]
        }
        vpn_config["hubs"].append(hub)

    response = requests.put(f"{BASE_URL}networks/{network_id}/appliance/vpn/siteToSiteVpn", json=vpn_config, headers=headers)

    if response.status_code == 200:
        print("VPN configuration updated successfully.")
    else:
        print("Failed to update VPN configuration.")

def main():
    api_key = input("Enter your Meraki API key: ")
    organization_id = input("Enter your Organization ID: ")

    # List networks
    networks = list_networks(api_key, organization_id)
    if not networks:
        return

    network_id = input("Enter the Network ID you want to configure: ")

    # Get VPN information for the selected network
    vpn_info = get_vpn_info(api_key, network_id)
    if not vpn_info:
        return

    print("Current VPN Configuration:")
    print(json.dumps(vpn_info, indent=4))

    # Ask the user for the order of hubs (hub IDs)
    print("Enter the order of hub IDs (comma-separated, e.g., 'N_682858293500168001,N_682858293500164378'): ")
    hubs_order = input().split(',')

    # Update VPN configuration
    update_vpn_config(api_key, network_id, vpn_info, hubs_order)

if __name__ == "__main__":
    main()
