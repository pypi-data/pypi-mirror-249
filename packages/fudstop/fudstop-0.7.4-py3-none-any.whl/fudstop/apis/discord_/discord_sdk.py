from . import *
class DiscordSDK(DiscordDBManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """
        A toolkit for working with the discord API.

        Your token is retrieved from the developer tools window. 

        >>> Network tab:

        Type a message in a channel while the dev. tools window is open with the 
        "Network" tab selected and filtered by "FETCH/XHR". 


        >>> URL:

        After typing the message - you'll see a URL pop up. Click on it - and scroll 
        down until you see the "Request Headers" section.
        
        Look for "authorization" and copy the token beside it, and paste it into an .env file as YOUR_DISCORD_HTTP_TOKEN=.
        """

    def connect_to_database(self, user:str='chuck', port:int=5432, password:str='fud', host:str='localhost', database:str='markets'):
        """
        Arguments:

        >>> db_config:

         **PASS IN YOUR POSTGRESQL CONFIG INFO:

         >>> database: the database name
         >>> host: the host (localhost)
         >>> port: the port (5432)
         >>> user: your user
         >>> password: your db password
        """
        # Define database connection parameters
        database = "markets"
        user = "chuck"
        port = 5432
        password = "fud"
        host = "localhost"

        # Create a database connection using psycopg2
        try:
            connection = psycopg2.connect(
                database=database,
                user=user,
                port=port,
                password=password,
                host=host
            )
            return connection
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)
            return None
    def get_roles(self, guild_id, role_id):
        """Gets role information for a guild. Use role_counts to get the role IDs."""
        url=f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}"
        r = requests.patch(url, headers=self.headers).json()

        return r
    def search(self, author_id:str='375862240601047070', has:str='file'):
        """Searches discord message history
        
        >>> author_id: the id of the author to search

        >>> has: file, embed, link, mentions, image..
        """
        offset = 0
        while True:
            time.sleep(5)
            offset = offset + 25
            url=f"https://discord.com/api/v9/guilds/888488311927242753/messages/search?author_id={author_id}&has={has}&offset={offset}"
            r = requests.get(url, headers=self.headers).json()


            messages = Messages(r)


            attachments = messages.attachments
            attachments = [item for sublist in attachments for item in sublist]

            attachments = Attachments(attachments)

            # Assuming attachments.filename is your list of filenames
            ogg_filenames = [file for file in attachments.filename if file.endswith('.ogg')]
        
            # Now, create or modify the DataFrame
            # If attachments.as_dataframe() provides the full DataFrame, filter it using the ogg_filenames list
            if hasattr(attachments, 'as_dataframe'):
                full_df = attachments.as_dataframe
                # Filter the DataFrame to include only rows with .ogg filenames
                ogg_df = full_df[full_df['filename'].isin(ogg_filenames)]

                for i,row in ogg_df.iterrows():
                    url = row['proxy_url']

                    yield url

            


    def sanitize_filename(self, filename):
        return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '.', '_', '-')]).rstrip()

    def get_unique_filename(self, set1, set2, directory):
        max_attempts = 10
        for _ in range(max_attempts):
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            random_part = f"{random.choice(set1)}f{random.choice(set2)}"
            filename = f"{current_time}_{random_part}.ogg"
            if not os.path.exists(os.path.join(directory, self.sanitize_filename(filename))):
                return filename
        raise Exception("Failed to generate a unique filename after several attempts")



    def download_voice_messages(self):
        set1 = ['A', 'R', 'G', 'B', 'C', 'Q', 'S', 'T', 'B', 'V']
        set2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for url in self.search():
            print(f"Processing URL: {url}")

            try:
                response = requests.get(url)

                if response.status_code == 200:
                    directory_path = f"messages/{datetime.datetime.now().strftime('%Y%m%d')}"
                    os.makedirs(directory_path, exist_ok=True)

                    filename = self.get_unique_filename(set1, set2, directory_path)
                    file_path = os.path.join(directory_path, self.sanitize_filename(filename))

                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded: {file_path}")
                else:
                    print(f"Failed to download from {url}: Status code {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading from {url}: {e}")
            except Exception as e:
                print(f"Error: {e}")

    def role_counts(self, guild_id):
        url=f"https://discord.com/api/v9/guilds/{guild_id}/roles/member-counts"
        r = requests.get(url, headers=self.headers).json()
        for i in r:
            print(i)

    def create_channel(self, guild_id, name, type='4', channel_description:str=None, with_webhook:bool=False, webhook_name:str=None):
        """
        Create a channel in a Discord guild.
        
        Args:
            >>> guild_id (str): The ID of the guild where the channel will be created.
            >>> name (str): The name of the channel.
            >>> type (str): The type of channel ('0' for text, '4' for category, '2' for voice, ''). Defaults to '4'.
        
        Returns:
            Response from the Discord API.
        """

        # Generate permission_overwrites from self.role_dict
        permission_overwrites = [{
            "id": role_id,
            "type": 0,
            "deny": "0",
            "allow": "71453223935041"
        } for role_id in self.role_dict.values()]

        # Prepare the payload
        payload = {
            "type": type,
            "name": name,
            "description": channel_description,
            "permission_overwrites": permission_overwrites
        }

        # Make the API request to create the channel
        r = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=self.headers, data=json.dumps(payload))

        id = r.json()['id']


        if with_webhook != False and name is not None:
            self.create_webhook(channel_id=id, name=webhook_name)

        


    def application_commands(self, guild):
        """
        >>> Returns: applications_df and commands_df

        >>> usage: applications, commands = application_commands(guild)
        
        """
        url=f"https://discord.com/api/v9/guilds/{guild}/application-command-index"
        r = requests.get(url, headers=self.headers).json()
        applications = Applications(r['applications'])
        application_commands = r['application_commands']
        commands = ApplicationCommands(application_commands)

        applications_df = applications.applications_as_dataframe
        commands_df = commands.as_dataframe



        return applications_df, commands_df


    def get_webhooks(self, guild_id):
        url=f"https://discord.com/api/v9/guilds/{guild_id}/webhooks"
        r = requests.get(url, headers=self.headers).json()


        webhooks = Webhooks(r)


        return webhooks.as_dataframe
    


    def create_webhook(self, channel_id, name):
        """
        Create a webhook in a Discord channel.

        This function sends a POST request to the Discord API to create a webhook
        in the specified channel with the provided name.

        :param channel_id: The ID of the Discord channel where the webhook will be created.
        :param name: The name of the webhook to be created.
        :return: A JSON response containing information about the created webhook.
        """
        url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
        payload = {'name': name}
        r = requests.post(url, headers=self.headers, data=json.dumps(payload))

        return r.json()


    def delete_channel(self, channel_id):
        
        url = f"https://discord.com/api/v9/channels/{channel_id}"


        r = requests.delete(url=url, headers=self.headers)


        return r
    
    def create_thread(self, channel_id:str="1193718649404538980", name:str="YOUR THREAD NAME HERE", topic:str='YOUR DESCRIPTION HERE', nsfw:bool=False, invitable:bool=True, locked:bool=False):
        connection = self.connect_to_database()
        self.create_thread_table(connection=connection)
        payload = {"name":name,"type":11,"topic":topic,"bitrate":64000,"user_limit":0,"nsfw":nsfw,"flags":0,"rate_limit_per_user":0,"auto_archive_duration":10080,"locked": locked,"invitable":invitable}
        r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/threads", headers=self.headers, data=json.dumps(payload)).json()

        thread_id = r.get('id')
        parent_channel = r.get('parent_id')
        name = r.get('name')
        total_messages = r.get('total_messages_sent')
        message_count = r.get('message_count')
        last_message_id = r.get('last_message_id')
        guild = r.get('guild_id')

        # Insert the retrieved attributes into the database
        self.insert_thread(thread_id, parent_channel, name, total_messages, message_count, last_message_id, guild)


        

    def upload_file(self, channel_id, file_path):
        random_id = random.randint(1, 9223372036854775807)
        file_size = os.path.getsize(file_path)
        url=f"https://discord.com/api/v9/channels/{channel_id}/attachments"

        payload = {"files":[{"filename":file_path,"file_size":file_size,"id":random_id,"is_clip":False}]}
        
        r = requests.post(url, headers=self.headers, data=json.dumps(payload)).json()
        
        attachments = r['attachments']

        upload_url = [i.get('upload_url') for i in attachments]

        return upload_url
    
