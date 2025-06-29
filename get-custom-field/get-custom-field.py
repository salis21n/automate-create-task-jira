import requests
import json
import os
import base64
from dotenv import load_dotenv

# Muat environment variables dari file .env
load_dotenv() 

# --- Konfigurasi ---
JIRA_URL = "https://your_url_jira.atlassian.net"  # Ganti dengan URL Jira Anda
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN") 
JIRA_EMAIL = os.getenv("JIRA_EMAIL")       

# --- Fungsi Autentikasi ---
def get_auth_headers():
    if not JIRA_API_TOKEN or not JIRA_EMAIL:
        print("Error: JIRA_API_TOKEN and JIRA_EMAIL environment variables must be set in .env file.")
        exit(1) 

    auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    encoded_auth_string = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    return {
        "Authorization": f"Basic {encoded_auth_string}",
        "Accept": "application/json",
        "Content-Type": "application/json" # Tambahkan ini jika Anda akan melakukan POST
    }

# --- Fungsi untuk mendapatkan Custom Fields (dari kode sebelumnya) ---
def get_custom_fields():
    headers = get_auth_headers()
    url = f"{JIRA_URL}/rest/api/3/field"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching custom fields: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        exit(1)

# --- Fungsi BARU: Mendapatkan Transisi yang Tersedia untuk Isu ---
def get_available_transitions(issue_key_or_id):
    headers = get_auth_headers()
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key_or_id}/transitions"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transitions for issue {issue_key_or_id}: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        return None

# --- Main Program ---
if __name__ == "__main__":
    # --- Bagian Custom Fields (dari kode sebelumnya) ---
    print("--- Mendapatkan Custom Field IDs ---")
    fields = get_custom_fields()
    if fields:
        print("Daftar Custom Field ID beserta Nama dan Tipe:")
        print("---------------------------------------------------------------------------------------------------")
        print(f"{'ID':<20} | {'Nama Field':<40} | {'Tipe Skema':<20}")
        print("---------------------------------------------------------------------------------------------------")
        for field in fields:
            if field.get("custom") == True:
                field_id = field.get("id")
                field_name = field.get("name")
                schema_type = field.get("schema", {}).get("type", "N/A")
                if field_name == "Epic Link" or field_name == "Epic Name":
                    print(f"{field_id:<20} | {field_name:<40} | {schema_type:<20} (contoh: untuk kode epic)")
                else:
                    print(f"{field_id:<20} | {field_name:<40} | {schema_type:<20}")
        print("---------------------------------------------------------------------------------------------------")
    else:
        print("Gagal mengambil custom fields.")
    
    print("\n" + "="*80 + "\n") # Pemisah

    # --- Bagian BARU: Mendapatkan Transisi ---
    print("--- Mendapatkan Informasi Transisi ---")
    # Ganti 'SYS-50' dengan Issue Key dari tugas yang ingin Anda cek transisinya
    # Pastikan isu ini berada di status 'Backlog' atau 'To Do' untuk melihat transisi ke 'Done'.
    issue_to_check = "SYS-50" 
    transitions_data = get_available_transitions(issue_to_check)

    if transitions_data and "transitions" in transitions_data:
        print(f"Transisi yang tersedia untuk isu '{issue_to_check}':")
        print("----------------------------------------------------")
        print(f"{'ID Transisi':<15} | {'Nama Transisi':<25} | {'Status Tujuan':<20}")
        print("----------------------------------------------------")
        for transition in transitions_data["transitions"]:
            transition_id = transition.get("id")
            transition_name = transition.get("name")
            to_status_name = transition.get("to", {}).get("name")
            
            print(f"{transition_id:<15} | {transition_name:<25} | {to_status_name:<20}")
            
            # Cek jika ini adalah transisi ke 'Done'
            if to_status_name and to_status_name.lower() == "done":
                print(f"   >>> Ini adalah transisi ke status 'Done'. ID yang dicari: {transition_id}, Nama: {transition_name}")
                
        print("----------------------------------------------------")
    else:
        print(f"Gagal mendapatkan transisi untuk isu '{issue_to_check}'.")
        if transitions_data and "errorMessages" in transitions_data:
            print(f"Error: {transitions_data['errorMessages']}")