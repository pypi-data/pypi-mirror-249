import requests
from bs4 import BeautifulSoup
import json

class JiraHelper:
    def __init__(self, server_url, email, api_token):
        self.server_url = server_url.rstrip('/')
        self.auth = (email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_ticket(self, project_key, summary, description, issue_type):
        """
        Create a ticket in a specified project using the provided details.

        :param project_key: Key of the project where the new ticket will be created.
        :param summary: Summary of the new ticket.
        :param description: Detailed description of the new ticket.
        :param issue_type: Type of the issue (e.g., Bug, Task, Story).
        :return: URL of the created ticket or False if the creation failed.
        """
        # Preparing issue data
        print("Preparing issue data...")
        issue_data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
            }
        }

        # Making a request to create a ticket
        print(f"Sending request to create a ticket in project {project_key}...")
        response = requests.post(
            f"{self.server_url}/rest/api/2/issue",
            json=issue_data,
            headers=self.headers,
            auth=self.auth,
            params={"some_param_key": "some_param_value"}  # Replace with desired params
        )

        # Checking response
        if response.status_code == 201:  # HTTP 201 Created
            print("Ticket created successfully!")
            ticket_data = response.json()
            ticket_key = ticket_data["key"]
            ticket_url = f"{self.server_url}/browse/{ticket_key}"
            print(f"Ticket URL: {ticket_url}")

            return ticket_url
        else:
            print(f"Failed to create ticket. HTTP Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            return False

    def delete_ticket(self, ticket_key):
        if not self.if_ticket_exist(ticket_key):
            return False

        response = requests.delete(
            f"{self.server_url}/rest/api/2/issue/{ticket_key}",
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code == 204:  # HTTP 204 No Content, indicates success.
            return True
        else:
            return False

    import requests

    def get_transitions(self, ticket_key, transition_to):
        """
        Retrieve the transition ID for a given ticket based on the desired transition name.

        :param ticket_key: Key of the ticket for which transitions are being fetched.
        :param transition_to: Desired transition name to look for.
        :return: Transition ID if found, or False if not found or if request failed.
        """
        # Making a request to get transitions

        response = requests.get(
            f"{self.server_url}/rest/api/2/issue/{ticket_key}/transitions",
            headers=self.headers,
            auth=self.auth
        )

        # Checking response
        if response.status_code == 200:  # HTTP 200 OK
            print("Successfully fetched transitions!")
            transitions = response.json().get("transitions", [])
            for transition in transitions:
                if str(transition["name"]).lower() == transition_to.lower():
                    print(f"Found transition '{transition_to}' with ID: {transition['id']}")
                    return transition["id"]
            print(f"Transition '{transition_to}' not found for ticket: {ticket_key}")
            return False
        else:
            print(f"Failed to fetch transitions. HTTP Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            return False

    def transition_ticket(self, ticket_key, transition_input):
        """
        Transition a ticket based on the provided input which can be a transition name or ID.

        :param ticket_key: Key of the ticket to be transitioned.
        :param transition_input: Desired transition name or ID to perform on the ticket.
        :return: True if the transition was successful, or False otherwise.
        """
        # Check if the transition input is an ID or a name
        print(f"Attempting to transition ticket: {ticket_key}...")
        if str(transition_input).isdigit():
            print("Using provided transition ID.")
            transition_id = transition_input
        else:
            print(f"Fetching transition ID for '{transition_input}'...")
            transition_id = self.get_transitions(ticket_key, str(transition_input).lower())
            if not transition_id:
                print(f"Failed to find a transition ID for '{transition_input}'!")
                return False

        # Prepare the payload and make a request to transition the ticket
        payload = {
            "transition": {
                "id": transition_id
            }
        }

        response = requests.post(
            f"{self.server_url}/rest/api/2/issue/{ticket_key}/transitions",
            headers=self.headers,
            auth=self.auth,
            json=payload
        )

        # Checking response
        if response.status_code == 204:  # HTTP 204 No Content, indicates success.
            print(f"Successfully transitioned ticket: {ticket_key}")
            return True
        else:
            print(f"Failed to transition ticket. HTTP Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            return False

    def if_ticket_exist(self, ticket_key):
        """
        Check if a ticket with the provided key exists.

        :param ticket_key: Key of the ticket to be checked.
        :return: True if the ticket exists, or False otherwise.
        """
        # Making a request to check if the ticket exists
        print(f"Checking existence of ticket: {ticket_key}...")
        response = requests.get(
            f"{self.server_url}/rest/api/2/issue/{ticket_key}",
            headers=self.headers,
            auth=self.auth
        )

        # Evaluating the response
        if response.status_code == 200:  # HTTP 200 OK, indicates the ticket exists.
            print(f"Ticket {ticket_key} exists!")
            return True
        elif response.status_code == 404:  # HTTP 404 Not Found, indicates the ticket does not exist.
            print(f"Ticket {ticket_key} does not exist!")
            return False
        else:
            print(f"Failed to verify ticket existence. HTTP Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            return False

    def comment_ticket(self, ticket_key, comment_text):
        """
        Add a comment to a ticket with the provided key.

        :param ticket_key: Key of the ticket where the comment will be added.
        :param comment_text: Text of the comment to be added.
        :return: URL of the created comment if successful, or False otherwise.
        """
        # Checking if the ticket exists
        if not self.if_ticket_exist(ticket_key):
            return False

        # Preparing the payload to add the comment
        print(f"Adding comment to ticket: {ticket_key}...")
        payload = {
            "body": comment_text
        }

        response = requests.post(
            f"{self.server_url}/rest/api/2/issue/{ticket_key}/comment",
            headers=self.headers,
            auth=self.auth,
            json=payload
        )

        # Evaluating the response
        if response.status_code == 201:  # HTTP 201 Created, indicates success.
            comment_id = response.json().get("id")
            comment_url = f"{self.server_url}/browse/{ticket_key}?focusedCommentId={comment_id}#comment-{comment_id}"
            print(f"Successfully added comment to ticket {ticket_key}. Comment URL: {comment_url}")
            return comment_url
        else:
            print(
                f"Failed to add comment to ticket {ticket_key}. Status code: {response.status_code}, Response: {response.text}")
            return False

    def jql_ticket(self, jql_query, max_results=None):
        """
        Retrieve tickets based on a provided JQL query, up to a specified maximum number of results.

        :param jql_query: The Jira Query Language query string to retrieve tickets.
        :param max_results: The maximum number of tickets to retrieve. If not specified, fetches all tickets.
        :return: List of ticket keys if successful, or False otherwise.
        """
        all_ticket_keys = []
        start_at = 0
        batch_size = 50  # This number can be adjusted based on your preference

        print(f"Executing JQL query: '{jql_query}'...")

        while True:
            payload = {
                "jql": jql_query,
                "fields": ["key"],  # We only need the ticket key
                "maxResults": batch_size,
                "startAt": start_at
            }

            response = requests.post(
                f"{self.server_url}/rest/api/2/search",
                headers=self.headers,
                auth=self.auth,
                json=payload
            )

            if response.status_code == 200:  # HTTP 200 OK, indicates success.
                issues = response.json().get("issues", [])
                ticket_keys = [issue["key"] for issue in issues]
                all_ticket_keys.extend(ticket_keys)

                print(f"Fetched {len(ticket_keys)} tickets in this batch.")

                # Check if we need to fetch more results or if we've reached the limit if one was set
                if not max_results:
                    if len(issues) < batch_size:
                        break
                    else:
                        start_at += batch_size
                else:
                    if len(all_ticket_keys) >= max_results:
                        all_ticket_keys = all_ticket_keys[:max_results]
                        break
                    elif len(issues) < batch_size:
                        break
                    else:
                        start_at += batch_size
            else:
                print(f"Failed to fetch tickets. HTTP Status Code: {response.status_code}, Response: {response.text}")
                return False

        print(f"You requested to fetch: {len(all_ticket_keys)}")
        return all_ticket_keys

class WikiHelper:
    def __init__(self, server_url, email, api_token):
        self.server_url = server_url.rstrip('/') + "/wiki"
        self.auth = (email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_wiki_page(self, space_key, title, content, parent_page_id=None):
        """
        Create a Confluence wiki page in the specified space.

        :param space_key: Key of the Confluence space where the new page will reside.
        :param title: Title of the new page.
        :param content: Content of the new page.
        :param parent_page_id: Optional parent page ID if the new page is to be a child.
        :return: URL of the created Confluence page or None if creation failed.
        """
        page_data = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }

        if parent_page_id:
            page_data["ancestors"] = [{"id": parent_page_id}]

        print(f"Creating Confluence page with title '{title}' in space '{space_key}', please wait...")

        # Note: Ensure the endpoint matches your Confluence server URL if it differs from Jira's
        response = requests.post(
            f"{self.server_url}/rest/api/content",
            json=page_data,
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code == 200:  # HTTP 200 OK indicates success for Confluence.
            wiki_page_url = response.json().get("_links", {}).get("webui")
            if wiki_page_url:
                complete_url = f"{self.server_url}{wiki_page_url}"
                print(f"Page '{title}' created successfully! You can view it here: {complete_url}")
                return complete_url
            else:
                print(f"Page '{title}' created, but unable to retrieve the page URL.")
                return False
        else:
            print(f"Failed to create Confluence page. Status code: {response.status_code}, Response: {response.text}")
            return False

    import requests

    def duplicate_wiki_page(self, source_page_id, target_space_key, target_title, target_parent_page_id=None):
        """
        Duplicate a Confluence wiki page from a source page to a target space with a new title.

        :param source_page_id: ID of the source Confluence page to be duplicated.
        :param target_space_key: Key of the Confluence space where the duplicated page will reside.
        :param target_title: Title of the duplicated page.
        :param target_parent_page_id: Optional parent page ID if the duplicated page is to be a child.
        :return: URL of the duplicated Confluence page or None if duplication failed.
        """

        print(
            f"Initiating duplication of page with ID '{source_page_id}' to space '{target_space_key}' with title '{target_title}'...")

        # 1. Retrieve content from the source page
        response = requests.get(
            f"{self.server_url}/rest/api/content/{source_page_id}?expand=body.storage",
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code != 200:
            print(
                f"Failed to retrieve source page content. Status code: {response.status_code}, Response: {response.text}")
            return False

        source_content = response.json()["body"]["storage"]["value"]
        print(f"Successfully retrieved content from source page with ID '{source_page_id}'.")

        # 2. Create the new page using the content from the source page
        return self.create_wiki_page(target_space_key, target_title, source_content, target_parent_page_id)

    def create_page_from_template(self, template_id, space_key, title, parent_page_id=None):
        """
        Create a Confluence wiki page using a specified template.

        :param template_id: ID of the Confluence template to use.
        :param space_key: Key of the Confluence space where the new page will reside.
        :param title: Title of the new page.
        :param parent_page_id: Optional parent page ID if the new page is to be a child.
        :return: Created Confluence page object for the new page or None if failed.
        """

        print(f"Initiating creation of page '{title}' in space '{space_key}' using template ID '{template_id}'...")

        # Check if a page with the same title already exists
        duplicate_check_response = requests.get(
            f"{self.server_url}/rest/api/content?spaceKey={space_key}&title={title}",
            headers=self.headers,
            auth=self.auth
        )

        if duplicate_check_response.status_code == 200:
            pages = duplicate_check_response.json().get('results', [])
            if pages:
                print(f"A page with the title '{title}' already exists in space '{space_key}'.")
                return False

        # 1. Retrieve content from the template
        response = requests.get(
            f"{self.server_url}/rest/api/template/{template_id}",
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code != 200:
            print(
                f"Failed to retrieve content from template with ID '{template_id}'. Status code: {response.status_code}, Response: {response.text}")
            return False

        print(f"Successfully retrieved content from template with ID '{template_id}'.")

        template_content = response.json()["body"]["storage"]["value"]

        # 2. Create the new page using the content from the template
        print(f"Creating the new page '{title}' using the retrieved template content...")

        payload = {
            "type": "page",
            "title": title,
            "space": {
                "key": space_key
            },
            "body": {
                "storage": {
                    "value": template_content,
                    "representation": "storage"
                }
            }
        }

        if parent_page_id:
            payload["ancestors"] = [{"id": parent_page_id}]

        response = requests.post(
            f"{self.server_url}/rest/api/content/",
            headers=self.headers,
            auth=self.auth,
            json=payload
        )

        if response.status_code == 200 or response.status_code == 201:
            wiki_page_url = response.json().get("_links", {}).get("webui")
            if wiki_page_url:
                complete_url = f"{self.server_url}{wiki_page_url}"
                print(f"Page '{title}' successfully created in space '{space_key}'.")
                return complete_url
            else:
                print(f"Page '{title}' created, but unable to retrieve the page URL.")
                return False
        else:
            print(
                f"Failed to create page '{title}' from template. Status code: {response.status_code}, Response: {response.text}")
            return False

    def move_wiki_page(self, page_id, target_space_key, target_position='append', target_parent_page_id=None):
        """
        Move a Confluence wiki page to a new space and position within another page without changing its title.

        :param page_id: ID of the Confluence page to be moved.
        :param target_space_key: Key of the Confluence space where the moved page will reside.
        :param target_position: Position to place the moved page relative to the parent page
                                (e.g., 'append', 'above', 'below'). Default is 'append'.
        :param target_parent_page_id: Optional ID of the parent page in which the page will be moved under.
        :return: Moved Confluence page object for the page or None if move operation failed.
        """

        print(f"Initiating move of page with ID '{page_id}'...")

        # 1. Retrieve current title of the page
        response = requests.get(
            f"{self.server_url}/rest/api/content/{page_id}",
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code != 200:
            print(
                f"Failed to retrieve current title of page with ID '{page_id}'. Status code: {response.status_code}, Response: {response.text}")
            return None

        current_title = response.json()["title"]
        current_version = response.json()["version"]["number"]

        # 2. Construct the payload for the move operation
        print(f"Preparing to move page '{current_title}' to space '{target_space_key}'.")
        move_payload = {
            "id": page_id,
            "type": "page",
            "title": current_title,  # Use the current title
            "space": {"key": target_space_key},
            "version": {"number": current_version + 1},  # Assuming the first version, modify if different # Increment the version
            "position": target_position
        }

        if target_parent_page_id:
            move_payload["ancestors"] = [{"id": target_parent_page_id}]

        # 3. Make the request to move the page
        print(f"Executing move operation for page '{current_title}'...")
        response = requests.put(
            f"{self.server_url}/rest/api/content/{page_id}",
            headers=self.headers,
            auth=self.auth,
            json=move_payload
        )


        if response.status_code == 200:
            wiki_page_url = response.json().get("_links", {}).get("webui")
            if wiki_page_url:
                complete_url = f"{self.server_url}{wiki_page_url}"
                print(
                    f"Successfully moved page '{current_title}' to space '{target_space_key}'.")
                return complete_url
            else:
                print(f"Page moved, but unable to retrieve the page URL.")
                return False

        else:
            print(
                f"Failed to move page '{current_title}'. Status code: {response.status_code}, Response: {response.text}")
            return None

    def wiki_page_exists(self, title, space_key):
        """
        Check if a Confluence wiki page already exists based on its title and space key.

        :param title: Title of the Confluence wiki page.
        :param space_key: Key of the Confluence space.
        :return: True if the page exists, False otherwise.
        """

        print(f"Checking if wiki page '{title}' exists in space '{space_key}'...")

        jql_query = f'space="{space_key}" AND title="{title}"'
        endpoint_url = f"{self.server_url}/rest/api/content/search?cql={jql_query}"

        response = requests.get(
            endpoint_url,
            headers=self.headers,
            auth=self.auth
        )

        if response.status_code == 200:
            results = response.json()["results"]
            if len(results) > 0:
                print(f"Wiki page '{title}' exists in space '{space_key}'.")
                return True
            else:
                print(f"Wiki page '{title}' does not exist in space '{space_key}'.")
                return False
        else:
            print(
                f"Failed to check wiki page existence. Status code: {response.status_code}, Response: {response.text}")
            return False

    def get_child_pages_recursive(self, parent_id):
        """
        Recursively retrieve all descendant pages of a given parent page ID.

        :param parent_id: ID of the parent Confluence wiki page.
        :return: List of child pages with their titles and IDs.
        """

        def fetch_children(page_id):
            endpoint_url = f"{self.server_url}/rest/api/content/{page_id}/child/page"
            response = requests.get(
                endpoint_url,
                headers=self.headers,
                auth=self.auth
            )

            if response.status_code == 200:
                children = response.json().get("results", [])
                simplified_children = [{"id": child["id"], "title": child["title"], "parentid": page_id} for child in
                                       children]
                return simplified_children
            else:
                print(f"Failed to fetch children for page ID {page_id}. Status: {response.status_code}.")
                return []

        children = fetch_children(parent_id)
        all_pages = children.copy()

        for child in children:
            all_pages.extend(self.get_child_pages_recursive(child["id"]))

        return all_pages

    def get_page_id(self, title, space_key):
        """
        Retrieve the ID of a Confluence wiki page by its title.

        :param title: Title of the Confluence wiki page.
        :param space_key: Key of the Confluence space to search in.
        :return: ID of the page if found, otherwise None.
        """
        print(f"Searching for page with title: {title} in space: {space_key}...")

        endpoint_url = f"{self.server_url}/rest/api/content"
        params = {
            "title": title,  # search by title
            "spaceKey": space_key,  # search in the specific space
            "limit": 1,  # we are only interested in one page with the exact title
        }

        response = requests.get(
            endpoint_url,
            headers=self.headers,
            auth=self.auth,
            params=params
        )

        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                page_id = results[0].get("id")
                print(f"Page found! ID: {page_id}")
                return page_id
            else:
                print(f"No page found with title: {title} in space: {space_key}")
                return False
        else:
            print(
                f"Failed to search for page with title {title} in space {space_key}. Status code: {response.status_code}, Response: {response.text}")
            return False

    def replace_in_page(self, page_id, from_string, to_string):
        """
        Replace all occurrences of a string in a Confluence wiki page.

        :param page_id: ID of the Confluence wiki page.
        :param from_string: String to be replaced.
        :param to_string: String to replace with.
        :return: True if replacement was successful, False otherwise.
        """

        print(f"Fetching content of page ID: {page_id}...")

        endpoint_url = f"{self.server_url}/rest/api/content/{page_id}"
        params = {"expand": "version,body.storage"}

        response = requests.get(
            endpoint_url,
            headers=self.headers,
            auth=self.auth,
            params=params
        )

        if response.status_code != 200:
            print(f"Failed to fetch page content. Status code: {response.status_code}, Response: {response.text}")
            return False

        page_data = response.json()
        content = page_data["body"]["storage"]["value"]

        print("Performing replacements...")
        updated_content = content.replace(from_string, to_string)

        if updated_content == content:
            print(f"No occurrences of '{from_string}' found in page ID: {page_id}")
            return True

        new_version = page_data["version"]["number"] + 1
        update_payload = {
            "version": {"number": new_version},
            "title": page_data["title"],
            "type": "page",
            "body": {"storage": {"value": updated_content, "representation": "storage"}},
        }

        print("Updating page with new content...")
        response = requests.put(
            endpoint_url,
            headers=self.headers,
            auth=self.auth,
            json=update_payload
        )

        if response.status_code == 200:
            print(f"Page ID: {page_id} updated successfully!")
            return True
        else:
            print(f"Failed to update page content. Status code: {response.status_code}, Response: {response.text}")
            return False

    from bs4 import BeautifulSoup

    def get_tables_from_page(self, page_id):
        """
        Fetch all tables from a Confluence wiki page based on the provided page ID and convert them into a structured JSON.

        :param page_id: ID of the Confluence wiki page.
        :return: A JSON structure containing all tables from the page.
        """

        print(f"Fetching content of page ID: {page_id}...")

        endpoint_url = f"{self.server_url}/rest/api/content/{page_id}"
        params = {"expand": "body.storage"}

        response = requests.get(
            endpoint_url,
            headers=self.headers,
            auth=self.auth,
            params=params
        )

        if response.status_code != 200:
            print(f"Failed to fetch page data. Status code: {response.status_code}, Response: {response.text}")
            return json.dumps({})

        page_content = response.json()['body']['storage']['value']
        soup = BeautifulSoup(page_content, 'html.parser')

        tables = soup.find_all('table')

        result = {}
        for idx, table in enumerate(tables, start=1):
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            rows = table.find_all("tr")[1:]  # skipping the header row
            row_data = []
            for row in rows:
                values = [td.get_text(strip=True) for td in row.find_all("td")]
                row_dict = dict(zip(headers, values))
                row_data.append(row_dict)
            result[f"table{idx}"] = row_data

        return json.dumps(result)