#!/usr/bin/env python3
"""
Script to add descriptive comments to all docker-compose.yaml files in the Docker folder.
"""

import os
import re
from pathlib import Path

# Service descriptions - mapping service names to descriptions
SERVICE_DESCRIPTIONS = {
    'ollama': 'Ollama - Local LLM inference server',
    'lobe-chat': 'Lobe Chat - Web UI for interacting with LLM models',
    'actual_server': 'Actual - Personal finance management application',
    'adguard': 'AdGuard Home - DNS-level ad blocker',
    'airconnect': 'AirConnect - AirPlay to Chromecast bridge',
    'appwrite': 'Appwrite - Backend-as-a-Service platform',
    'radarr': 'Radarr - Movie collection manager and downloader',
    'sonarr': 'Sonarr - TV series collection manager and downloader',
    'bazarr': 'Bazarr - Subtitle manager for Radarr and Sonarr',
    'jellyfin': 'Jellyfin - Media server for movies, TV shows and music',
    'jellyseerr': 'Jellyseerr - Content request management for Jellyfin',
    'pihole': 'Pi-hole - Network-wide DNS ad blocker',
    'traefik': 'Traefik - Reverse proxy and load balancer',
    'whoami': 'Whoami - Test service for Traefik routing',
    'jackett': 'Jackett - Torrent indexer aggregator',
    'prowlarr': 'Prowlarr - Indexer manager for arr-stack',
    'qbittorrent': 'qBittorrent - Torrent client',
    'transmission': 'Transmission - Lightweight torrent client',
    'plex': 'Plex Media Server - Media streaming service',
    'emby': 'Emby - Alternative media server',
    'nextcloud': 'Nextcloud - Self-hosted file sharing and collaboration',
    'synology': 'Synology - NAS integration',
    'home-assistant': 'Home Assistant - Home automation platform',
    'homeassistant': 'Home Assistant - Home automation platform',
    'grafana': 'Grafana - Metrics visualization and monitoring',
    'prometheus': 'Prometheus - Metrics collection and monitoring',
    'influxdb': 'InfluxDB - Time-series database',
    'telegraf': 'Telegraf - Metrics collection agent',
    'loki': 'Loki - Log aggregation system',
    'gitea': 'Gitea - Self-hosted Git service',
    'gitlab': 'GitLab - DevOps platform',
    'github': 'GitHub - Version control and collaboration',
    'vaultwarden': 'Vaultwarden - Bitwarden-compatible password manager',
    'bitwarden': 'Bitwarden - Password manager',
    'authelia': 'Authelia - Authentication and authorization server',
    'keycloak': 'Keycloak - Identity and access management',
    'freshrss': 'FreshRSS - RSS feed aggregator',
    'miniflux': 'Miniflux - RSS feed reader',
    'wallabag': 'Wallabag - Article bookmarking and reading service',
    'paperless': 'Paperless - Document management system',
    'photoprism': 'PhotoPrism - AI-powered photo management service',
    'immich': 'Immich - Self-hosted photo and video backup solution',
    'synology-photos': 'Synology Photos - Photo management for Synology',
    'calibre': 'Calibre - E-book library management',
    'kavita': 'Kavita - Manga and comic book server',
    'komga': 'Komga - Manga server',
    'myherolist': 'MyHeroList - Anime/Manga tracking',
    'uptime_kuma': 'Uptime Kuma - Self-hosted uptime monitoring',
    'status-page': 'Status Page - System status page',
    'speedtest': 'Speedtest - Internet speed testing service',
    'mattermost': 'Mattermost - Self-hosted team collaboration platform',
    'rocketchat': 'Rocket.Chat - Self-hosted instant messaging platform',
    'discord-bot': 'Discord Bot - Custom Discord bot',
    'synology': 'Synology - NAS integration service',
    'duplicati': 'Duplicati - Backup and restore utility',
    'veeam': 'Veeam - Backup and recovery software',
    'restic': 'Restic - Fast and secure backup solution',
    'couchdb': 'CouchDB - NoSQL document database',
    'mongodb': 'MongoDB - NoSQL database',
    'mysql': 'MySQL - Relational database',
    'mariadb': 'MariaDB - MySQL-compatible relational database',
    'postgres': 'PostgreSQL - Advanced relational database',
    'redis': 'Redis - In-memory data structure store',
    'elasticsearch': 'Elasticsearch - Search and analytics engine',
    'opensearch': 'OpenSearch - Open-source search engine',
    'minio': 'MinIO - S3-compatible object storage',
    'mailserver': 'Mail Server - Email service',
    'postfix': 'Postfix - Mail transfer agent',
    'dovecot': 'Dovecot - Mail delivery and authentication',
    'roundcube': 'Roundcube - Webmail client',
    'code-server': 'Code Server - VS Code in the browser',
    'coder': 'Coder - Workspace-as-Code platform',
    'vscode': 'VS Code - Code editor',
    'filebrowser': 'File Browser - Web-based file manager',
    'guacamole': 'Apache Guacamole - Clientless remote desktop',
    'vnc': 'VNC Server - Remote desktop access',
    'x11vnc': 'x11VNC - VNC server for X11 displays',
    'wireguard': 'WireGuard - Modern VPN protocol',
    'openvpn': 'OpenVPN - VPN tunnel solution',
    'tailscale': 'Tailscale - Managed mesh VPN',
    'ddclient': 'ddclient - Dynamic DNS update client',
    'duckdns': 'DuckDNS - Free DDNS service',
    'npm': 'Nginx Proxy Manager - Reverse proxy management UI',
    'swag': 'SWAG - Nginx reverse proxy with Let\'s Encrypt',
    'caddy': 'Caddy - Automatic HTTPS web server',
    'nginx': 'Nginx - Web server and reverse proxy',
    'apache': 'Apache - Web server',
    'httpd': 'Apache HTTP Server',
    'wordpress': 'WordPress - CMS and blogging platform',
    'drupal': 'Drupal - CMS platform',
    'joomla': 'Joomla - CMS platform',
    'mediawiki': 'MediaWiki - Wiki engine',
    'dokuwiki': 'DokuWiki - Lightweight wiki',
    'confluence': 'Confluence - Team content collaboration',
    'wiki': 'Wiki - Knowledge base',
    'tiddlywiki': 'TiddlyWiki - Non-linear personal web notebook',
    'bookstack': 'BookStack - Self-hosted documentation platform',
    'outline': 'Outline - Team knowledge base',
    'obsidian': 'Obsidian - Note-taking and knowledge management',
    'joplin': 'Joplin - Note-taking application',
    'memos': 'Memos - Lightweight note-taking service',
    'logseq': 'LogSeq - Privacy-first knowledge management',
    'trilium': 'Trilium Notes - Knowledge management system',
    'zendrive': 'Zendrive - File sync and backup',
    'syncthing': 'Syncthing - Continuous file synchronization',
    'storj': 'Storj - Decentralized cloud storage',
    'seafile': 'Seafile - Cloud storage and file collaboration',
    'owncloud': 'Nextcloud/OwnCloud - File sync and share',
    'pydio': 'Pydio - File sharing platform',
    'gitea': 'Gitea - Self-hosted Git service',
    'forgejo': 'Forgejo - Lightweight Git service',
    'gitbucket': 'GitBucket - Git platform',
    'gogs': 'Gogs - Painless self-hosted Git service',
    'gitolite': 'Gitolite - Git repository hosting',
    'comfyui': 'ComfyUI - Stable Diffusion UI',
    'stable-diffusion': 'Stable Diffusion - AI image generation',
    'sd-webui': 'Stable Diffusion WebUI - Stable Diffusion interface',
    'ollama': 'Ollama - Local LLM inference server',
    'text-generation-webui': 'Text Generation WebUI - LLM interface',
    'llamagpt': 'LlamaGPT - GPT interface using Llama',
    'chatgpt': 'ChatGPT - OpenAI integration',
    'langchain': 'LangChain - LLM application framework',
    'anything-llm': 'AnythingLLM - RAG and AI chat',
    'gpt4all': 'GPT4All - Free LLM runner',
    'jan': 'Jan - AI chat application',
    'january': 'January - AI assistant',
    'influxdb': 'InfluxDB - Time-series database',
    'timescaledb': 'TimescaleDB - PostgreSQL time-series extension',
    'victoriametrics': 'VictoriaMetrics - Time-series database',
    'm3db': 'M3DB - Distributed time-series database',
    'grafana-loki': 'Grafana Loki - Log aggregation',
    'vector': 'Vector - Data pipeline platform',
    'filebeat': 'Filebeat - Log shipping',
    'logstash': 'Logstash - Data processing pipeline',
    'fluentd': 'Fluentd - Data collector and processor',
    'td-agent': 'Fluentd (td-agent) - Data collector',
    'rsyslog': 'Rsyslog - System logging daemon',
    'syslog-ng': 'Syslog-ng - System event and log processing',
    'splunk': 'Splunk - Data analytics platform',
    'sumologic': 'Sumo Logic - Cloud monitoring platform',
    'datadog': 'Datadog - Monitoring and analytics platform',
    'newrelic': 'New Relic - Application performance monitoring',
    'dynatrace': 'Dynatrace - Application performance management',
    'sentry': 'Sentry - Error tracking and monitoring',
    'elastic': 'Elasticsearch - Search and analytics',
    'kibana': 'Kibana - Elasticsearch visualization',
    'beats': 'Elastic Beats - Data shippers',
    'apm': 'Elastic APM - Application performance monitoring',
    'odoo': 'Odoo - Business management software',
    'shopware': 'Shopware - E-commerce platform',
    'woocommerce': 'WooCommerce - WordPress e-commerce',
    'prestashop': 'PrestaShop - E-commerce platform',
    'magento': 'Magento - E-commerce platform',
    'opencart': 'OpenCart - E-commerce platform',
    'zencart': 'Zen Cart - E-commerce platform',
    'oscommerce': 'osCommerce - E-commerce platform',
    'saleor': 'Saleor - Headless e-commerce',
    'medusa': 'Medusa - Open-source commerce platform',
    'supabase': 'Supabase - Firebase alternative',
    'firebase': 'Firebase - Backend-as-a-Service',
    'parse': 'Parse - Backend-as-a-Service',
    'nocodb': 'NocoDB - Open-source Airtable alternative',
    'airtable': 'Airtable - Collaborative spreadsheet',
    'budibase': 'Budibase - Low-code application builder',
    'appsmith': 'Appsmith - Low-code application development',
    'retool': 'Retool - Internal tools builder',
    'illa': 'ILLA - Low-code tool builder',
    'openblocks': 'OpenBlocks - Open-source app builder',
    'refine': 'Refine - React framework for admin apps',
    'n8n': 'n8n - Workflow automation tool',
    'make': 'Make (Integromat) - Integration platform',
    'zapier': 'Zapier - Automation and integration',
    'ifttt': 'IFTTT - Automation service',
    'huginn': 'Huginn - Automation and monitoring',
    'patreon': 'Patreon - Creator funding platform',
    'plausible': 'Plausible - Privacy-focused analytics',
    'umami': 'Umami - Privacy-focused analytics',
    'fathom': 'Fathom - Privacy-first analytics',
    'simple-analytics': 'Simple Analytics - Privacy analytics',
    'goatcounter': 'GoatCounter - Simple analytics',
    'open-analytics': 'Open Analytics - Analytics platform',
    'mixpanel': 'Mixpanel - Product analytics',
    'amplitude': 'Amplitude - Product intelligence',
    'segment': 'Segment - Customer data platform',
    'rudderstack': 'RudderStack - Open-source CDP',
    'mparticle': 'mParticle - Customer data platform',
    'twilio': 'Twilio - Communication platform',
    'vonage': 'Vonage - Communication APIs',
    'sendgrid': 'SendGrid - Email delivery platform',
    'mailgun': 'Mailgun - Email API',
    'sparkpost': 'SparkPost - Email service provider',
    'sendpulse': 'SendPulse - Marketing automation',
    'mailchimp': 'Mailchimp - Email marketing',
    'brevo': 'Brevo (Sendinblue) - Marketing platform',
    'getresponse': 'GetResponse - Marketing automation',
    'aweber': 'AWeber - Email marketing',
    'drip': 'Drip - Marketing automation',
    'klaviyo': 'Klaviyo - E-commerce marketing',
    'constant-contact': 'Constant Contact - Email marketing',
    'pardot': 'Pardot - Marketing automation',
    'marketo': 'Marketo - Marketing automation',
    'hubspot': 'HubSpot - CRM and marketing',
    'salesforce': 'Salesforce - CRM platform',
    'zoho': 'Zoho - Business software suite',
    'pipedrive': 'Pipedrive - Sales CRM',
    'freshsales': 'Freshsales - CRM software',
    'insightly': 'Insightly - CRM and project management',
    'creatio': 'Creatio - Low-code business automation',
    'sugarcrm': 'SugarCRM - Customer relationship management',
    'agilecrm': 'Agile CRM - Sales and marketing automation',
    'copper': 'Copper - Gmail-first CRM',
    'streak': 'Streak - CRM for Gmail',
    'waffle': 'Waffle - Team collaboration tool',
    'plane': 'Plane - Project management',
    'plane-web': 'Plane Web - Project management UI',
    'jira': 'Jira - Issue tracking and project management',
    'trello': 'Trello - Kanban board',
    'asana': 'Asana - Work management platform',
    'monday': 'Monday.com - Work operating system',
    'notion': 'Notion - All-in-one workspace',
    'coda': 'Coda - Document collaboration',
    'fibery': 'Fibery - Work management',
    'clickup': 'ClickUp - All-in-one work management',
    'todoist': 'Todoist - Task management',
    'things': 'Things - Personal task management',
    'reminders': 'Reminders - Task tracking',
    'any-do': 'Any.do - Task and habit management',
    'wunderbucket': 'Wunderbucket - Habit tracking',
    'habitica': 'Habitica - Gamified task and habit tracker',
    'sentry': 'Sentry - Error tracking',
    'rollbar': 'Rollbar - Error tracking and monitoring',
    'bugsnag': 'Bugsnag - Error and crash monitoring',
    'airbrake': 'Airbrake - Error monitoring',
    'honeybadger': 'Honeybadger - Error monitoring',
    'exception-alert': 'Exception Alert - Error monitoring',
    'raygun': 'Raygun - Error monitoring',
    'crashlytics': 'Crashlytics - Crash reporting',
    'apptentive': 'Apptentive - User feedback and engagement',
    'delighted': 'Delighted - Customer feedback',
    'typeform': 'Typeform - Online forms and surveys',
    'hotjar': 'Hotjar - Heatmaps and feedback',
    'fullstory': 'FullStory - Digital experience analytics',
    'logrocket': 'LogRocket - Frontend monitoring',
    'smartlook': 'Smartlook - Session recording',
    'glassbox': 'Glassbox - Digital experience analytics',
    'contentsquare': 'Contentsquare - Digital analytics',
}

def get_service_description(service_name):
    """Get description for a service, return default if not found."""
    name_lower = service_name.lower()
    if name_lower in SERVICE_DESCRIPTIONS:
        return SERVICE_DESCRIPTIONS[name_lower]
    # Return a generic description based on service name
    return f"{service_name.title()} - Docker service"

def add_header_comment(content, folder_name):
    """Add a header comment to the docker-compose file."""
    # Map folder name to description
    service_map = {
        'actual': 'Actual - Personal finance management',
        'adguard': 'AdGuard Home - DNS-level ad blocker',
        'ai': 'AI services - Ollama LLM and Lobe Chat UI',
        'aircast': 'AirCast - AirPlay to Chromecast bridge',
        'appwrite': 'Appwrite - Backend-as-a-Service platform',
        'arr': 'Arr Stack - Radarr, Sonarr, Bazarr (media management)',
        'azuracast': 'AzuraCast - Self-hosted radio automation',
        'bb': 'Big Brother - Monitoring service',
        'betterforever': 'Better Forever - Service',
        'budibase': 'Budibase - Low-code application builder',
        'changedetection': 'Changedetection - Website change detector',
        'code-server': 'Code Server - VS Code in browser',
        'coder': 'Coder - Workspace-as-Code platform',
        'comfyui': 'ComfyUI - Stable Diffusion UI',
        'copyparty': 'Copyparty - File sharing service',
        'couchdb': 'CouchDB - NoSQL document database',
        'crafty': 'Crafty - Minecraft server manager',
        'cryptgeon': 'Cryptgeon - Encrypted message passing',
        'dashy': 'Dashy - Dashboard and homepage',
        'ddclient': 'ddclient - Dynamic DNS update client',
        'ddns': 'DDNS - Dynamic DNS services',
        'discord': 'Discord - Chat and communication',
        'docker-wyze-bridge': 'Wyze Bridge - Wyze camera integration',
        'doku': 'Doku - Documentation platform',
        'doplarr': 'Doplarr - Discord media management bot',
        'duplicati': 'Duplicati - Backup and restore',
        'ersatz': 'Ersatz - Service',
        'ferdium': 'Ferdium - Multi-account messaging',
        'filebrowser': 'File Browser - Web file manager',
        'flame': 'Flame - Hotplate-like dashboard',
        'freshrss': 'FreshRSS - RSS feed aggregator',
        'glance': 'Glance - Personal dashboard',
        'GoAccess': 'GoAccess - Web analytics tool',
        'grafana': 'Grafana - Metrics visualization',
        'grocy': 'Grocy - Grocery management',
        'homarr': 'Homarr - Homepage and dashboard',
        'homeassistant': 'Home Assistant - Home automation',
        'homepage': 'Homepage - Dashboard and launcher',
        'immich': 'Immich - Photo and video backup',
        'it-tools': 'IT Tools - Utilities collection',
        'jackett': 'Jackett - Torrent indexer aggregator',
        'january': 'January - AI assistant',
        'jdownloader-2': 'JDownloader 2 - Download manager',
        'jellyfin': 'Jellyfin - Media server',
        'jellyseerr': 'Jellyseerr - Content request manager',
        'jfa-go': 'jfa-go - Jellyfin account manager',
        'kavita': 'Kavita - Manga and comic server',
        'kitchenowl': 'KitchenOwl - Recipe manager',
        'komga': 'Komga - Manga server',
        'llamagpt': 'LlamaGPT - GPT interface',
        'magma': 'Magma - Service',
        'maybe': 'Maybe - Finance planning tool',
        'memos': 'Memos - Note-taking service',
        'minecraft': 'Minecraft - Game server',
        'minecraft-january': 'Minecraft January - Game server',
        'minecraft-mexicrew': 'Minecraft MexiCrew - Game server',
        'minecraftforge': 'Minecraft Forge - Modded server',
        'minecraftserver': 'Minecraft Server - Standard server',
        'mongodb': 'MongoDB - NoSQL database',
        'mstream': 'mStream - Music streaming',
        'mylar': 'Mylar - Comic book manager',
        'navidrome': 'Navidrome - Music server',
        'nextcloud': 'Nextcloud - File sync and share',
        'NPM': 'Nginx Proxy Manager - Reverse proxy UI',
        'oasis': 'Oasis - Service',
        'octoprint': 'OctoPrint - 3D printer web interface',
        'ollama': 'Ollama - LLM inference server',
        'openbooks': 'OpenBooks - Book collection browser',
        'overseerr': 'Overseerr - Content request management',
        'palworld': 'Palworld - Game server',
        'paperless': 'Paperless - Document management',
        'perpetual-summer': 'Perpetual Summer - Service',
        'pihole': 'Pi-hole - DNS ad blocker',
        'plausible': 'Plausible - Privacy-focused analytics',
        'plex': 'Plex Media Server - Media streaming',
        'plex-meta-manager': 'Plex Meta Manager - Library automation',
        'printer': 'Printer - Printer integration',
        'prowlarr': 'Prowlarr - Indexer manager',
        'qbittorrent': 'qBittorrent - Torrent client',
        'radarr': 'Radarr - Movie manager',
        'rss': 'RSS - Feed services',
        'scrypted': 'Scrypted - HomeKit and security integration',
        'search': 'Search - Search services',
        'sonarr': 'Sonarr - TV series manager',
        'speedtest': 'Speedtest - Internet speed testing',
        'spotify': 'Spotify - Music streaming',
        'stable-diffusion': 'Stable Diffusion - AI image generation',
        'stable-diffusion-webui': 'Stable Diffusion WebUI - AI image interface',
        'suwayomi': 'Suwayomi - Manga reader',
        'swag': 'SWAG - Nginx reverse proxy with SSL',
        'sygil': 'Sygil - AI image generation UI',
        'tachidesk': 'Tachidesk - Manga server',
        'tachidesk-alpine': 'Tachidesk Alpine - Lightweight manga server',
        'tailscale': 'Tailscale - Mesh VPN',
        'tdarr': 'Tdarr - Media transcoding',
        'text-generation-webui': 'Text Generation WebUI - LLM interface',
        'torrent': 'Torrent - Torrent services',
        'traefik': 'Traefik - Reverse proxy and load balancer',
        'umami': 'Umami - Privacy-focused analytics',
        'uptime_kuma': 'Uptime Kuma - Uptime monitoring',
        'utilities': 'Utilities - Helper services',
        'vocard': 'Vocard - Service',
        'wikijs': 'Wiki.js - Wiki engine',
        'winter-games': 'Winter Games - Game collection',
        'wireguard': 'WireGuard - VPN tunnel',
        'wordpress': 'WordPress - CMS platform',
        'youtube': 'YouTube - YouTube services',
    }
    
    description = service_map.get(folder_name.lower(), f"{folder_name} Service")
    header = f"# Docker Compose configuration for {description}\n\n"
    return header + content

def process_docker_compose_file(file_path):
    """Add comments to a docker-compose file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Skip if file already has header comment
        if content.strip().startswith('# Docker Compose configuration'):
            print(f"⏭️  Skipping (already commented): {file_path}")
            return False
        
        # Get folder name
        folder_name = file_path.parent.name
        
        # Add header comment
        new_content = add_header_comment(content, folder_name)
        
        # Add comments to service sections
        lines = new_content.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            result_lines.append(line)
            
            # Check if this line contains a service name
            if line.strip() and not line.strip().startswith('#') and ':' in line:
                stripped = line.strip()
                # Check if it's a service definition (not indented too much)
                if stripped.endswith(':') and line.startswith('  ') and not line.startswith('    '):
                    service_name = stripped.rstrip(':').strip()
                    # Check if service name looks valid (no special chars)
                    if service_name and service_name.isidentifier() or '-' in service_name:
                        description = get_service_description(service_name)
                        # Add comment before service
                        indent = len(line) - len(line.lstrip())
                        result_lines.insert(-1, ' ' * indent + f'# {description}')
            
            i += 1
        
        new_content = '\n'.join(result_lines)
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Process all docker-compose files in the Docker folder."""
    docker_dir = Path('/Users/jbpixel/Documents/GitHub/self-hosted-bmo/Docker')
    
    if not docker_dir.exists():
        print(f"Error: Docker directory not found at {docker_dir}")
        return
    
    # Find all docker-compose.yaml files
    compose_files = list(docker_dir.glob('**/docker-compose.yaml'))
    print(f"Found {len(compose_files)} docker-compose.yaml files\n")
    
    updated_count = 0
    for compose_file in sorted(compose_files):
        if process_docker_compose_file(compose_file):
            updated_count += 1
    
    print(f"\n✨ Summary: Updated {updated_count} files")

if __name__ == '__main__':
    main()
